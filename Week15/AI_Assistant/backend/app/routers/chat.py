from fastapi import APIRouter, HTTPException

from app.schemas import ChatRequest, ChatResponse
from app.providers import PROVIDER_REGISTRY

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    provider = PROVIDER_REGISTRY.get(req.provider)
    if provider is None:
        raise HTTPException(status_code=400, detail=f"Unknown provider '{req.provider}'")
    return await provider.chat(req)