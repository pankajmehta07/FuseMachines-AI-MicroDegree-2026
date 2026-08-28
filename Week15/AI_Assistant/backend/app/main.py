from fastapi import FastAPI

from app.routers import health, chat, structured

app = FastAPI(title="AI Assistant", version="0.3.0")

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(structured.router)