"""
postprocessor.py
Format and polish raw LLM outputs into natural Indonesian answers.
- Ensures clarity, removes artifacts
- Adds short citations for RAG answers if available
"""

import re

def clean_output(text: str) -> str:
    """
    Clean up common LLM artifacts: extra spaces, unwanted tokens.
    """
    if not text:
        return ""

    # Remove multiple spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stray markdown artifacts
    text = text.replace("```", "").replace("###", "").strip()

    return text


def format_sql_answer(raw_answer: str) -> str:
    """
    Post-process SQL answers: ensure short, natural Indonesian.
    Example: "Papua 2022 1.9" -> "Pada tahun 2022, angka kelahiran di Papua tercatat sebesar 1.9."
    """
    answer = clean_output(raw_answer)

    # Optionally enforce first letter uppercase
    if answer and not answer[0].isupper():
        answer = answer[0].upper() + answer[1:]

    return answer


def format_rag_answer(raw_answer: str, citation: str = None) -> str:
    """
    Post-process RAG answers: natural tone + optional short citation.
    Example: "Ya, terdapat aturan..." + "(Perda No. 12/2021)"
    """
    answer = clean_output(raw_answer)

    # Add short citation if provided and not already in the text
    if citation and citation not in answer:
        answer = f"{answer} ({citation})"

    return answer
