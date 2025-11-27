import os
import torch
import subprocess

# ======== HARDWARE SETTINGS =========
# Flag for CPU vs GPU
USE_GPU = True
DEVICE = "cuda" if USE_GPU and torch.cuda.is_available() else "cpu"

print(f"[CONFIG] Running on: {DEVICE.upper()}")

# ======== SERVICE CHECKS =========
def check_service(command, name, timeout=3):
    """Run a command to check if a service is active (with timeout)."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        if result.returncode == 0:
            print(f"[CONFIG] {name} is running ✅")
        else:
            print(f"[CONFIG] {name} is NOT running ❌")
    except subprocess.TimeoutExpired:
        print(f"[CONFIG] {name} check timed out ⏱️")
    except Exception as e:
        print(f"[CONFIG] {name} check failed: {e}")

# Check Ollama (default port 11434)
check_service("ollama ps", "Ollama")

# Check Docker (basic check)
check_service("docker info >nul 2>&1" if os.name == "nt" else "docker info > /dev/null 2>&1", "Docker")


# ======== DATA SETTINGS =========
DATASET_PATH = r"C:\Users\Legion\OneDrive\Documents\Kompas\kompas-chatbot-project\data\raw\Dataset_UU_Final.parquet"
MASTER_LOC_PATH = r"C:\Users\Legion\OneDrive\Documents\Kompas\kompas-chatbot-project\data\raw\master_loc.xlsx"

# ======== EMBEDDING SETTINGS =========
# Recommended embeddings:
# - "nomic-embed-text" (1536-dim, accurate, good for legal text)
# - "all-MiniLM-L6-v2" (384-dim, fast, good for stats/numeric queries)
EMB_MODEL = os.getenv("EMB_MODEL", "nomic-embed-text")
EMB_BATCH_SIZE = 64
EMB_DIM = 768

# ======== LLM SETTINGS =========
# Choices (via Ollama or HuggingFace):
# - "qwen2.5:3b-instruct" → small, efficient, sometimes stiff
# - "qwen2.5:7b-instruct" → more natural fluency, still reasonable
# - "qwen2.5:3b-instruct-q4_K_M" → quantized and speed priority 
# - "gemma:2b-instruct" → lightweight, good Indonesian fluency
# - "mistral:7b-instruct" → strong fluency, heavier
LLM_ID = os.getenv("LLM_ID", "qwen2.5:3b-instruct")

# ======== QDRANT SETTINGS =========
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
COLLECTION_NAME = "legal_docs"

# ======== PROMPT TEMPLATES =========
SYSTEM_INSTRUCTIONS = (
    "Kamu adalah asisten hukum Indonesia. "
    "Jawab HANYA berdasarkan dokumen yang tersedia. "
    "Jika tidak ada informasi yang cukup, katakan 'Tidak ditemukan dalam data'. "
    "Gunakan Bahasa Indonesia formal, jelas, dan alami. "
)

RAG_PROMPT_TEMPLATE = """
Anda adalah asisten hukum.
Gunakan dokumen berikut untuk menjawab pertanyaan secara alami dan percakapan.
Cantumkan sumber dokumen singkat di akhir jika memungkinkan.

Dokumen:
{context}

Pertanyaan: {query}

Jawaban (dalam Bahasa Indonesia yang alami):
"""

SQL_PROMPT_TEMPLATE = """
Anda adalah asisten data.
Gunakan hasil berikut untuk menjawab pertanyaan secara alami, ringkas, dan jelas.

Hasil Query:
{result}

Pertanyaan: {query}

Jawaban (dalam Bahasa Indonesia yang alami):
"""

# ======== RETRIEVAL SETTINGS =========
TOP_K = 5  # how many docs to retrieve in RAG
