# chatbot_project/nlp/embedding.py
import numpy as np
from functools import lru_cache
import ollama

EMB_MODEL = "nomic-embed-text"


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


class Embedder:
    """Wrapper with caching so embeddings aren’t recomputed."""

    def __init__(self, model: str = EMB_MODEL):
        self.model = model

    @lru_cache(maxsize=20000)
    def _get_tuple(self, text: str):
        resp = ollama.embeddings(model=self.model, prompt=text)
        vec = np.array(resp["embedding"], dtype=np.float32)
        return tuple(vec.tolist())

    def get_embedding(self, text: str) -> np.ndarray:
        return np.array(self._get_tuple(text), dtype=np.float32)

    def similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return _cosine(a, b)
