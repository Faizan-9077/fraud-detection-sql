# llm/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Provider Selection
LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
)

# Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3"

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"