import httpx

from app.config import LOCAL_LLM_URL, LOCAL_LLM_MODEL, SYSTEM_PROMPT
from app.schemas import ChatRequest, ChatResponse
from app.providers.base import LLMProvider


class LocalProvider(LLMProvider):
    async def chat(self, req: ChatRequest) -> ChatResponse:
        payload = {
            "model": LOCAL_LLM_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": req.message},
            ],
            "stream": False,
            "options": {
                "temperature": req.temperature,
                "top_p": req.top_p,
            },
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{LOCAL_LLM_URL}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            reply = data["message"]["content"]
            return ChatResponse(provider="local", model=LOCAL_LLM_MODEL, reply=reply)