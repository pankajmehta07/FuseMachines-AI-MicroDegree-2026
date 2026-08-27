from openai import OpenAI
from fastapi import HTTPException

from app.config import OPENAI_API_KEY, OPENAI_MODEL, SYSTEM_PROMPT
from app.schemas import ChatRequest, ChatResponse
from app.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    async def chat(self, req: ChatRequest) -> ChatResponse:
        if not self._client:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

        completion = self._client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": req.message},
            ],
            temperature=req.temperature,
            top_p=req.top_p,
            max_tokens=req.max_tokens,
        )
        reply = completion.choices[0].message.content
        return ChatResponse(provider="openai", model=OPENAI_MODEL, reply=reply)