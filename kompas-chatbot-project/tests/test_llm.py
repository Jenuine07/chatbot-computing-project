import pytest
from llm import llm_manager, prompts

def test_llm_generation():
    prompt = prompts.PROMPT_SQL_EXPLAIN.format(result="Papua | 2022 | 1.9", query="Berapa angka kelahiran di Papua?")
    answer = llm_manager.generate(prompt)
    assert isinstance(answer, str)
    print("\n🟩 LLM Output:", answer)
