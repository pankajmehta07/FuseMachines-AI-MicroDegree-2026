from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.reliability.rate_limiter import limiter
from app.routers import health, chat, structured, rag

app = FastAPI(title="AI Assistant", version="0.5.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(structured.router)
app.include_router(rag.router)