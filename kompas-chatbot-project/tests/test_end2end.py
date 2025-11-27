import pytest
from pipeline import hybrid_router

def test_full_pipeline():
    queries = [
        "Berapa angka kelahiran di Papua tahun 2022?",
        "Apakah ada aturan tentang pajak reklame di Sukabumi?",
        "Bagaimana ketentuan ekspor kayu di Papua tahun 2002?"
    ]

    for q in queries:
        print(f"\n🟨 Query: {q}")
        answer = hybrid_router.run(q)
        assert isinstance(answer, str)
        print("🟩 Answer:", answer)
