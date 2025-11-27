import pytest
from retrieval import retriever
from llm import llm_manager, prompts, postprocessor

def test_rag_pipeline():
    query = "Apakah ada aturan tentang pajak reklame di Sukabumi?"
    metadata = {"province": "jawa barat", "year": 2021, "category": "pajak daerah"}

    # Retrieve top-k context
    results = retriever.retrieve(query, metadata, top_k=3)
    assert results, "No RAG results found"

    # Build prompt
    context = "\n\n".join(r["payload"].get("judul_bersih", "") for r in results)
    prompt = prompts.PROMPT_RAG_ID.format(context=context, query=query)

    # Generate natural answer
    answer = llm_manager.generate(prompt)
    answer = postprocessor.format_rag_answer(answer)

    assert isinstance(answer, str)
    print("\n🟩 RAG Answer:", answer)
