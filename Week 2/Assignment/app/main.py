from fastapi import FastAPI, Depends
from database import get_db
from sqlalchemy.orm import Session
from database import Base, engine
import router as router
import counts_router as counts_router
from logger import get_logger

logger = get_logger(__name__)

Base.metadata.create_all(bind = engine)
logger.info("Database tables verified/created")


app = FastAPI(title="Classicmodels API",
    description="API for managing customers, orders and payments",
    version="1.0.0")

logger.info("FastAPI application started")

app.include_router(counts_router.router)
app.include_router(router.router)

@app.get("/")
def home(db: Session = Depends(get_db)):
    logger.info("Health check endpoint called")
    return {"message":"Customer API is running"}