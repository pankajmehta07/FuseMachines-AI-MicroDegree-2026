from typing import Literal, Optional, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message to the assistant")
    provider: Literal["openai", "local", "gemini"] = "local"
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    max_tokens: int = Field(512, gt=0, le=4096)
    use_tools: bool = Field(False, description="Allow the model to call tools")


class ChatResponse(BaseModel):
    provider: str
    model: str
    reply: str
    tool_calls: Optional[list[dict[str, Any]]] = None


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


class TaskExtractionRequest(BaseModel):
    text: str = Field(..., description="Free text describing a task, e.g. an email or note")
    provider: Literal["openai", "local", "gemini"] = "local"


class ExtractedTask(BaseModel):
    task_title: str = Field(..., description="Short title of the task")
    assignee: Optional[str] = Field(None, description="Person responsible, if mentioned")
    due_date: Optional[str] = Field(None, description="Due date if mentioned, in YYYY-MM-DD or as stated")
    priority: Literal["low", "medium", "high"] = Field("medium", description="Inferred urgency")
    tags: list[str] = Field(default_factory=list, description="Relevant short keywords")


class TaskExtractionResponse(BaseModel):
    provider: str
    model: str
    extracted: ExtractedTask