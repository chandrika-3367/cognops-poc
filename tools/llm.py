import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def call_llm(user_input: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.3,
        "max_tokens": 600,
        "top_p": 0.9,
        "stream": False
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Groq LLM ERROR] {str(e)}"
