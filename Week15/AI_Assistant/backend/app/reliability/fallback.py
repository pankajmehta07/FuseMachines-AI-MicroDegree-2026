"""
Tries a prioritized list of providers in order. If one fails, logs it
and tries the next, instead of failing the whole request.
"""
import logging

from app.providers import PROVIDER_REGISTRY
from app.schemas import ChatRequest, ChatResponse
from app.reliability.retry import with_retry

logger = logging.getLogger("reliability.fallback")

# Order matters: try local first (free, always available if Ollama's up),
# then Gemini (free tier), then OpenAI last (paid, may be quota-blocked).
DEFAULT_FALLBACK_ORDER = ["local", "gemini", "openai"]


@with_retry(max_attempts=2, base_delay=1.0)
async def _call_provider(provider_name: str, req: ChatRequest) -> ChatResponse:
    provider = PROVIDER_REGISTRY[provider_name]
    # Build a fresh request with the target provider, keeping all other settings
    provider_req = req.model_copy(update={"provider": provider_name})
    return await provider.chat(provider_req)


async def chat_with_fallback(req: ChatRequest, fallback_order: list[str] | None = None) -> ChatResponse:
    """
    Tries req.provider first (with retry). If it fails after retries,
    tries the remaining providers in fallback_order, skipping any
    already-tried provider.
    """
    order = fallback_order or DEFAULT_FALLBACK_ORDER
    # Put the user's requested provider first, then the rest as fallback
    providers_to_try = [req.provider] + [p for p in order if p != req.provider]

    errors = {}
    for provider_name in providers_to_try:
        try:
            response = await _call_provider(provider_name, req)
            if provider_name != req.provider:
                logger.info(f"Fell back from '{req.provider}' to '{provider_name}' successfully")
            return response
        except Exception as e:
            errors[provider_name] = str(e)
            logger.warning(f"Provider '{provider_name}' failed: {e}")

    # Every provider failed
    raise RuntimeError(f"All providers failed. Errors: {errors}")