from abc import ABC, abstractmethod
from app.schemas import ChatRequest, ChatResponse


class LLMProvider(ABC):
    """
    Common interface all LLM providers must implement.
    This is what makes swapping/adding providers (Step-2 OpenAI/local,
    later fallback logic in Task 2) a matter of adding a new class,
    not rewriting the router.
    """

    @abstractmethod
    async def chat(self, req: ChatRequest) -> ChatResponse:
        ...