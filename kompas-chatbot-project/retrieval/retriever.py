# retrieval/retriever.py

from typing import Dict, Any, List
from retrieval.metadata_filter import normalize_metadata, build_filter
from nlp.embedding import Embedder

embedder = Embedder()

def retrieve(query: str, metadata: Dict[str, Any], top_k: int = 5) -> List[Dict[str, Any]]:
    
    from retrieval.vector_store import search
    
    query_vector = embedder.get_embedding(query)
    filters = normalize_metadata(metadata or {})

    hits = search(query_vector=query_vector, qdrant_filter=build_filter(filters), top_k=top_k)

    if not hits and "tahun" in filters:
        relaxed = {k: v for k, v in filters.items() if k != "tahun"}
        hits = search(query_vector=query_vector, qdrant_filter=build_filter(relaxed), top_k=top_k)
        if hits:
            print("⚠️ Relaxed filter: dropped tahun")

    if not hits and "kategori" in filters:
        relaxed = {k: v for k, v in filters.items() if k != "kategori"}
        hits = search(query_vector=query_vector, qdrant_filter=build_filter(relaxed), top_k=top_k)
        if hits:
            print("⚠️ Relaxed filter: dropped kategori")

    results = []
    for hit in hits:
        payload = hit.payload or {}
        judul = payload.get("judul_bersih", "")
        tentang = payload.get("tentang", "")
        body = payload.get("body", "")

        snippet = body[:1000] + "..." if len(body) > 1000 else body

        context_text = f"{judul}\nTentang: {tentang}\nIsi Penting:\n{snippet}"

        results.append({
            "score": float(getattr(hit, "score", 0.0)),
            "id": getattr(hit, "id", None),
            "context": context_text,
            "payload": payload,
        })

    return results
