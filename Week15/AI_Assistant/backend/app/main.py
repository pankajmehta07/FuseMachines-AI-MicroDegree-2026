import os
import httpx
from fastapi import FastAPI

app = FastAPI(title="AI Assistant - Step 1 Skeleton")

LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://ollama:11434")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen2.5-coder:3b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.get("/health")
def health():
    """Basic liveness check for the backend container itself."""
    return {"status": "ok", "service": "backend"}


@app.get("/health/local-llm")
async def health_local_llm():
    """
    Checks that the backend container can reach the Ollama container
    over the internal Docker network.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{LOCAL_LLM_URL}/api/tags")
            resp.raise_for_status()
            models = [m["name"] for m in resp.json().get("models", [])]
            return {
                "status": "ok",
                "reachable": True,
                "configured_model": LOCAL_LLM_MODEL,
                "models_available_locally": models,
            }
    except Exception as e:
        return {"status": "error", "reachable": False, "detail": str(e)}


@app.get("/health/openai")
def health_openai():
    """
    Just confirms the API key is loaded into the container.
    Doesn't call OpenAI yet - actual API call comes in Step 2.
    """
    return {
        "status": "ok" if OPENAI_API_KEY else "missing_key",
        "key_loaded": bool(OPENAI_API_KEY),
    }