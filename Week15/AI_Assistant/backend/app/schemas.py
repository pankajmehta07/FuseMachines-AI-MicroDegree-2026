from typing import Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message to the assistant")
    provider: Literal["openai", "local", "gemini"] = "local"
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    max_tokens: int = Field(512, gt=0, le=4096)


class ChatResponse(BaseModel):
    provider: str
    model: str
    reply: str


class HealthResponse(BaseModel):
    status: str
    service: str


class LocalLLMHealthResponse(BaseModel):
    status: str
    reachable: bool
    configured_model: str | None = None
    models_available_locally: list[str] | None = None
    detail: str | None = None


class OpenAIHealthResponse(BaseModel):
    status: str
    key_loaded: bool


class GeminiHealthResponse(BaseModel):
    status: str
    key_loaded: bool