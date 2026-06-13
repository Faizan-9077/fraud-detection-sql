import requests

from .config import OLLAMA_BASE_URL, MODEL_NAME


class LlamaClient:
    def __init__(self):
        self.api_url = f"{OLLAMA_BASE_URL}/api/generate"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.api_url,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]