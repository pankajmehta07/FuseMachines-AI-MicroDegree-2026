import os
from dotenv import load_dotenv

load_dotenv()

# Local LLM (Ollama)
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://ollama:11434")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen2.5-coder:3b")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Shared assistant behavior
SYSTEM_PROMPT = (
    "You are a helpful, concise AI assistant built for a coursework project. "
    "Answer clearly and directly. If you are not sure about something, say so "
    "instead of guessing."
)