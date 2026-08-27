from app.providers.openai_provider import OpenAIProvider
from app.providers.local_provider import LocalProvider
from app.providers.gemini_provider import GeminiProvider

PROVIDER_REGISTRY = {
    "openai": OpenAIProvider(),
    "local": LocalProvider(),
    "gemini": GeminiProvider(),
}