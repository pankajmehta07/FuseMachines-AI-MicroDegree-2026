import logging
from fastapi import APIRouter, HTTPException, Request

from app.schemas import ChatRequest, ChatResponse
from app.reliability.fallback import chat_with_fallback
from app.reliability.rate_limiter import limiter

logger = logging.getLogger("routers.chat")

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(req: ChatRequest, request: Request):
    try:
        return await chat_with_fallback(req)
    except Exception as e:
        logger.error(f"chat endpoint failed completely: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "All LLM providers are currently unavailable.",
                "hint": "Check provider API keys/quotas, or that the local Ollama service is running.",
            },
        )