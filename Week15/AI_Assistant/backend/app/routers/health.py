import httpx
from fastapi import APIRouter

from app.config import LOCAL_LLM_URL, LOCAL_LLM_MODEL, OPENAI_API_KEY, GEMINI_API_KEY
from app.schemas import (
    HealthResponse,
    LocalLLMHealthResponse,
    OpenAIHealthResponse,
    GeminiHealthResponse,
)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", service="backend")


@router.get("/local-llm", response_model=LocalLLMHealthResponse)
async def health_local_llm():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{LOCAL_LLM_URL}/api/tags")
            resp.raise_for_status()
            models = [m["name"] for m in resp.json().get("models", [])]
            return LocalLLMHealthResponse(
                status="ok",
                reachable=True,
                configured_model=LOCAL_LLM_MODEL,
                models_available_locally=models,
            )
    except Exception as e:
        return LocalLLMHealthResponse(status="error", reachable=False, detail=str(e))


@router.get("/openai", response_model=OpenAIHealthResponse)
def health_openai():
    return OpenAIHealthResponse(status="ok" if OPENAI_API_KEY else "missing_key", key_loaded=bool(OPENAI_API_KEY))


@router.get("/gemini", response_model=GeminiHealthResponse)
def health_gemini():
    return GeminiHealthResponse(status="ok" if GEMINI_API_KEY else "missing_key", key_loaded=bool(GEMINI_API_KEY))