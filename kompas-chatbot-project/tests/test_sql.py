import pytest
from database import excel_loader
from llm import llm_manager, prompts

def test_sql_pipeline():
    # Load dataset
    df = excel_loader.load_dataset()
    assert not df.empty, "Dataset failed to load"

    # Simulate a metadata query
    province, year, category = "papua", 2022, "angka kelahiran"
    result_rows = excel_loader.fetch_point(province, year, category)

    assert result_rows is not None, "No rows returned from Excel loader"

    # Wrap with prompt and send to LLM
    query = f"Berapa {category} di {province} tahun {year}?"
    prompt = prompts.PROMPT_SQL_EXPLAIN.format(result=result_rows, query=query)
    answer = llm_manager.generate(prompt)

    assert isinstance(answer, str)
    print("\n🟩 SQL Answer:", answer)
