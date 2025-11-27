"""
prompts.py
Prompt templates for different chatbot tasks:
- SQL explanation
- RAG (law/regulation answers)
- Intent classification (optional fallback)
"""

# --- SQL Path ---
PROMPT_SQL_EXPLAIN = """
Anda adalah asisten data.
Gunakan hasil berikut untuk menjawab pertanyaan secara alami, ringkas, dan jelas.

Hasil Query:
{result}

Pertanyaan: {query}

Jawaban (dalam Bahasa Indonesia yang alami):
"""

# --- RAG Path ---
PROMPT_RAG_ID = """
Anda adalah asisten hukum.
Gunakan dokumen berikut untuk menjawab pertanyaan secara alami.
Sertakan link sumber HANYA JIKA 'Link Sumber' tersedia dan bukan 'Tidak tersedia'.
JANGAN sebutkan 'link' atau 'tautan' jika 'Link Sumber' tertulis 'Tidak tersedia'.
JANGAN mengarang link.

Dokumen:
{context}

Pertanyaan: {query}

Jawaban (dalam Bahasa Indonesia yang alami):
"""

# --- Intent Classification (optional) ---
PROMPT_CLASSIFY = """
Klasifikasikan pertanyaan berikut ke dalam salah satu kategori:

- SQL (numeric/statistical)
- RAG (legal/textual)

Pertanyaan:
{query}

Jawaban (SQL atau RAG saja):
"""
