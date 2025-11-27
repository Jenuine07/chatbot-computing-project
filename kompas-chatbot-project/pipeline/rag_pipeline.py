# pipeline/rag_pipeline.py

import json, csv, pandas as pd
import re 
from nlp.keyword_extractor import KeywordExtractor
from retrieval.retriever import retrieve
from retrieval import metadata_filter
from llm.prompts import PROMPT_RAG_ID
from llm.llm_manager import generate

extractor = KeywordExtractor()

def _find_best_snippet(query: str, keywords: list, full_text: str, snippet_size: int = 2000) -> str:
    if not full_text:
        return "Tidak ada konten."

    match = re.search(re.escape(query), full_text, re.IGNORECASE)
    
    if not match:
        for keyword in keywords:
            if len(keyword) > 3: 
                match = re.search(re.escape(keyword), full_text, re.IGNORECASE)
                if match:
                    break 

    if match:
        start_index = match.start()
        
        snippet_half = snippet_size // 2
        start = max(0, start_index - snippet_half)
        end = min(len(full_text), start_index + snippet_half)
        
        if start == 0:
            end = min(len(full_text), snippet_size)
        if end == len(full_text):
            start = max(0, len(full_text) - snippet_size)
            
        return full_text[start:end] + "..."
    
    else:
        return full_text[:snippet_size] + "..."


def run_rag_pipeline(query: str, 
                     top_k: int = 5, 
                     debug: bool = False,
                     export: str = None) -> str:
    
    keywords = extractor.extract(query)
    search_terms = list(set([query] + keywords)) 
    
    metadata = metadata_filter.keywords_to_metadata(keywords)
    results = retrieve(query, metadata, top_k=top_k)

    if not results:
        context = "Tidak ada dokumen relevan yang ditemukan."
        if debug:
            print("⚠️ No results retrieved with metadata:", metadata)
    else:
        if export:
            rows = []
            for r in results:
                rows.append({
                    "score": r["score"],
                    "judul": r["payload"].get("judul_bersih", "-"),
                    "province": r["payload"].get("province"),
                    "year": r["payload"].get("year"),
                    "category": r["payload"].get("category"),
                    "link": r["payload"].get("link_final"),
                    "body": r["payload"].get("body_preview", ""), 
                })
            
            if export.endswith(".csv"):
                pd.DataFrame(rows).to_csv(export, index=False)
                if debug:
                    print(f"✅ Exported retrieved results to {export}")
            elif export.endswith(".json"):
                with open(export, "w", encoding="utf-8") as f:
                    json.dump(rows, f, ensure_ascii=False, indent=2)
                if debug:
                    print(f"✅ Exported retrieved results to {export}")
            pass
        
        context_parts = []
        for i, r in enumerate(results):
            payload = r.get('payload', {}) 
            
            title = payload.get('judul_bersih','-')
            year = payload.get('year','-')
            
            full_body = payload.get('body_preview', '') 

            llm_snippet = _find_best_snippet(query, search_terms, full_body, snippet_size=2000)
            
            if debug:
                print(f"--- DEBUG: Snippet for Doc [{i+1}] ({title}) ---")
                if llm_snippet:
                    print(llm_snippet)
                else:
                    print("[...BODY IS EMPTY IN PAYLOAD...]")
                print("--- END DEBUG SNIPPET ---")
            
            link = payload.get('link_final') 
            
            if link and (link.startswith('http://') or link.startswith('https://')):
                link_info = f"Link Sumber: {link}"
            else:
                link_info = "Link Sumber: Tidak tersedia"
            
            entry = (
                f"Dokumen [{i+1}]: {title} ({year})\n"
                f"{link_info}\n"
                f"Isi: {llm_snippet}" 
            )
            context_parts.append(entry)
        
        context = "\n\n---\n\n".join(context_parts)

    prompt = PROMPT_RAG_ID.format(context=context, query=query)
    answer = generate(prompt, max_new_tokens=1024)
    
    return answer
