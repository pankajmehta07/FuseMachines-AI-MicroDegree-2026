from fastapi import FastAPI

from app.routers import health, chat

app = FastAPI(title="AI Assistant", version="0.2.0")

app.include_router(health.router)
app.include_router(chat.router)