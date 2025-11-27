"""
llm_manager.py
Unified, efficient interface for generating text with Ollama LLM.
- Uses ollama.chat() directly (no subprocess overhead)
- Supports system + user prompts
- Returns clean natural language answers or detailed error messages
"""

import ollama
from config.settings import LLM_ID


def generate(prompt: str, system: str = None, max_new_tokens: int = 512) -> str:
    """
    Generate a response from Ollama.

    Args:
        prompt (str): The user prompt or query.
        system (str, optional): System instruction for the model (role).
        max_new_tokens (int): Maximum tokens to generate.

    Returns:
        str: Natural language answer or error message.
    """
    try:
        # Build messages
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # Call Ollama API
        resp = ollama.chat(
            model=LLM_ID,
            messages=messages,
            options={"num_predict": max_new_tokens}
        )

        if not resp or "message" not in resp:
            return "[LLM Error] Empty response from Ollama."

        return resp["message"]["content"].strip()

    except Exception as e:
        return f"[LLM Error] {str(e)}"
