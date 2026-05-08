from fastapi import FastAPI, Depends
from database import get_db
from sqlalchemy.orm import Session
from database import Base, engine
from router import router

Base.metadata.create_all(bind = engine)
print("Database tables verified/created")


app = FastAPI(title="Classicmodels API",
    description="API for managing customers, orders and payments",
    version="1.0.0")

print("FastAPI application started")

app.include_router(router)

@app.get("/")
def home(db: Session = Depends(get_db)):
    print("Health check endpoint called")
    return {"message":"Customer API is running"}