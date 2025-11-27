# retrieval/embedder.py

"""
Embedder module
Handles embeddings for dataset chunks and user queries.
Supports batching for efficiency.
"""

from typing import List
import ollama  # Ollama embeddings
from config.settings import EMB_MODEL


def embed_text(text: str) -> List[float]:
    """
    Generate embedding for a single text string.
    """
    if not text or not isinstance(text, str):
        return []

    response = ollama.embeddings(model=EMB_MODEL, prompt=text)
    return response["embedding"]


def embed_batch(texts: List[str], batch_size: int = 128) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts.
    Uses batching to speed up processing.
    
    Args:
        texts (List[str]): list of texts to embed
        batch_size (int): how many texts per batch
    
    Returns:
        List of embeddings (List[List[float]])
    """
    vectors = []
    total = len(texts)

    for i in range(0, total, batch_size):
        batch = [t if isinstance(t, str) else "" for t in texts[i:i+batch_size]]

        for t in batch:  # Ollama handles one at a time
            response = ollama.embeddings(model=EMB_MODEL, prompt=t)
            vectors.append(response["embedding"])

        print(f"⚡ Processed {min(i+batch_size, total)}/{total} embeddings")

    return vectors
