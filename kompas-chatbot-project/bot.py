from config import constants, settings
from database import excel_loader
from retrieval import vector_store, retriever, metadata_filter
from nlp import cleaner, keyword_extractor
from llm import llm_manager, prompts, postprocessor
from pipeline import rag_pipeline

from qdrant_client import QdrantClient
client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

print(settings.LLM_ID)

# 1. Ensure collection exists
vector_store.create_collection_if_missing(recreate=True)
# vector_store.create_collection_if_missing()

# 2. Create embeddings only if missing
vector_store.create_embeddings_if_missing(force=True)
# vector_store.create_embeddings_if_missing()

print(client.get_collections())
print(client.count("legal_docs"))

from retrieval.vector_store import collection_has_points
print("Has embeddings:", collection_has_points())
