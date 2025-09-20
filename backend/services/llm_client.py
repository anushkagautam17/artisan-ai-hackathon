# backend/services/llm_client.py
import os
import json
import re
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in environment (.env).")

import openai
openai.api_key = OPENAI_API_KEY

def get_completion(prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 500, temperature: float = 0.7):
    """
    Calls OpenAI ChatCompletion and returns the assistant text (str).
    Change model to one that supports multimodal if/when available.
    """
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp["choices"][0]["message"]["content"].strip()

def extract_first_json(text: str):
    """
    Try to find and parse the first JSON object in the model output.
    Returns (obj, raw_json_text) or (None, last_raw_text) if parsing failed.
    """
    match = re.search(r'(\{(?:.|\n)*\})', text)
    if not match:
        return None, text
    jtext = match.group(1)
    try:
        return json.loads(jtext), jtext
    except json.JSONDecodeError:
        # try to fix trailing commas
        jtext_fixed = re.sub(r',\s*}', '}', jtext)
        jtext_fixed = re.sub(r',\s*]', ']', jtext_fixed)
        try:
            return json.loads(jtext_fixed), jtext_fixed
        except Exception:
            return None, text
