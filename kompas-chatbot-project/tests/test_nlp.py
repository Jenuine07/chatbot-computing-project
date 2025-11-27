import pytest
from nlp import cleaner, keyword_extractor, intent_detector, metadata_extractor

def test_cleaner():
    text = "  Pajak__Daerah  "
    norm = cleaner.Cleaner().normalize_text(text)
    assert norm == "pajak daerah"

def test_keyword_extractor():
    extractor = keyword_extractor.KeywordExtractor()
    result = extractor.extract("Apakah ada aturan tentang pajak rokok di Jakarta 2021?")
    assert "jakarta" in result and "pajak" in result

def test_intent_detector():
    assert intent_detector.detect_intent("Berapa angka kelahiran di Papua?") == "SQL"
    assert intent_detector.detect_intent("Apakah ada peraturan tentang pajak reklame?") == "RAG"

def test_metadata_extractor():
    query = "Apakah ada peraturan pajak reklame di Papua tahun 2021?"
    metadata = metadata_extractor.extract_metadata(query)
    assert metadata["province"] == "papua"
    assert metadata["year"] == 2021
