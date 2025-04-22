from langchain.llms.base import LLM
from typing import List
import requests


class GroqLLM(LLM):
    def __init__(self, model="llama3-70b-8192", temperature=0.0, groq_api_key=None):
        self.model = model
        self.temperature = temperature
        # Replace or pull from env
        self.groq_api_key = GROQ_API_KEY or ""

    @property
    def _llm_type(self) -> str:
        return "custom_groq_llm"

    def _call(self, prompt: str, stop: List[str] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
