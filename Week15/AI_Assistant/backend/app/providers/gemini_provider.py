from google import genai
from fastapi import HTTPException

from app.config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT
from app.schemas import ChatRequest, ChatResponse
from app.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self):
        self._client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

    async def chat(self, req: ChatRequest) -> ChatResponse:
        if not self._client:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")

        response = self._client.models.generate_content(
            model=GEMINI_MODEL,
            contents=req.message,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": req.temperature,
                "top_p": req.top_p,
                "max_output_tokens": req.max_tokens,
            },
        )
        return ChatResponse(provider="gemini", model=GEMINI_MODEL, reply=response.text)