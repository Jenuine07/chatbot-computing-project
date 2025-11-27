# 🤖 Kompas Legal & Statistical Chatbot

A **hybrid RAG + SQL chatbot system** that can answer questions about **Indonesian laws, regulations, and regional statistics** using both structured and unstructured data.

Built for modularity, clarity, and extensibility — this system is the “brain” behind your private dataset chatbot.

---

## 🧠 Overview

This project combines:

* **RAG (Retrieval-Augmented Generation)** → for unstructured legal text (`body` column).
* **SQL/Numeric Querying** → for structured data (statistics, birth rates, etc.).
* **Hybrid Router** → auto-detects user intent and routes to the right pipeline.

---

## 📂 Project Structure

```
chatbot_project/
│
├── config/                 # Model configs, constants, and settings
├── data/                   # Datasets (Excel or SQL source)
├── database/               # Excel loader and SQL adapter
├── nlp/                    # Cleaning, keyword extraction, intent & metadata
├── retrieval/              # Embeddings, vector search, metadata filter
├── llm/                    # Prompt templates, LLM interface, post-processing
├── pipeline/               # SQL, RAG, and router pipelines (the brain)
├── app/                    # API & optional UI (FastAPI/Streamlit)
└── tests/                  # Unit & integration tests
```

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your_repo>/chatbot_project.git
   cd chatbot_project
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # (Linux/Mac)
   .venv\Scripts\activate      # (Windows)
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   * Create a `.env` file:

     ```
     QDRANT_URL=http://localhost:6333
     QDRANT_API_KEY=
     OLLAMA_HOST=http://localhost:11434
     ```
   * Adjust paths in `config/settings.py` as needed.

---

## 🧩 How It Works

### 1. **Intent Detection**

* Distinguishes between numeric/statistical queries and legal/textual queries.
* Example:

  * “Berapa angka kelahiran di Papua 2022?” → SQL Path
  * “Apakah ada aturan tentang pajak reklame di Sukabumi?” → RAG Path

### 2. **Metadata Extraction**

* Detects province, year(s), and category from natural queries.
* Uses `Cleaner`, `KeywordExtractor`, and mapping dictionaries.

### 3. **SQL Path**

* Filters Excel/SQL dataset by metadata.
* Returns numeric values → formatted with `PROMPT_SQL_EXPLAIN`.

### 4. **RAG Path**

* Applies metadata filters → retrieves relevant law chunks (`body` field).
* Passes context to LLM with `PROMPT_RAG_ID`.

### 5. **LLM Layer**

* Powered by local model (`qwen2.5-7b-instruct`, `gemma-2b`, or `mistral-7b`).
* Produces natural Indonesian responses.

---

## 🚀 Running the Chatbot

### 🧭 Option 1 — Command Line Interface

```bash
python -m app.ui
```

### 🖥️ Option 2 — FastAPI Server

```bash
uvicorn app.main:app --reload
```

Visit → [http://localhost:8000/docs](http://localhost:8000/docs) for API docs.

### 🧩 Option 3 — Streamlit UI

```bash
streamlit run app/ui.py
```

---

## 🧪 Testing

Run tests individually or all at once using `pytest`:

```bash
pytest -v
```

Tests include:

* `test_nlp.py` → keyword & intent extraction
* `test_sql.py` → data filtering + LLM explanation
* `test_rag.py` → retrieval + text response
* `test_end2end.py` → full hybrid routing

---

## ⚡ Performance Notes

* Embeddings are precomputed (no re-embedding each query).
* Metadata filters reduce retrieval cost.
* Fallback strategy relaxes filters if strict match yields no results.
* GPU acceleration is auto-detected (via `config/settings.py`).

---

## 🛠️ Configuration Reference

Edit these in `config/settings.py`:

```python
LLM_ID = "qwen2.5-7b-instruct"
EMB_MODEL = "nomic-embed-text"
COLLECTION_NAME = "legal_docs"
USE_GPU = True
DEVICE = "cuda" if USE_GPU else "cpu"
TOP_K = 5
```

---

## 📈 Example Interaction

**User:**

> Apakah ada aturan tentang ekspor kayu bulat di Papua tahun 2002?

**Bot:**

> Ya, terdapat *Keputusan Gubernur Papua Nomor 72 Tahun 2002* yang mengatur ketentuan ekspor kayu bulat jenis merbau di Papua.

---

## 🤝 Contributing

1. Fork this repo.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Commit changes and open a pull request.

---

## 📜 License

MIT License © 2025 Kompas Media Nusantara

---