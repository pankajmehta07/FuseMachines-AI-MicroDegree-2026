from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from database import get_db
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=List[schemas.customerOut])
def list_customers(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    logger.info(f"Get Customers - skip = {skip}, limit = {limit}")
    return crud.get_customers(db = db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=schemas.customerOut)
def get_customer(customer_id: int,db: Session = Depends(get_db)):
    logger.info(f"Get Customers - ID = {customer_id}")
    customer = crud.get_customer(db = db, id=customer_id)
    if customer is None:
        logger.error(f"Customer {customer_id} not found - returning 404")
        raise HTTPException(status_code=404, detail="Customer Not Found")

    return customer

@router.post("/", response_model=schemas.customerOut)
def create_customer(customer : schemas.customerCreate, db: Session = Depends(get_db)):
    logger.info(f"Create customer - {customer.customerName}")
    return crud.create_customer(db = db, customer=customer)

@router.put("/{customer_id}", response_model=schemas.customerOut)
def update_customer(customer_id:int, updates : schemas.customerUpdate, db: Session = Depends(get_db)):
    logger.info(f"UPDATE /customers/{customer_id}")
    updated = crud.update_customer(db = db, updates=updates, customer_id=customer_id)

    if updated is None:
        logger.error(f"Update Failed - customer {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return updated

@router.delete("/{customer_id}")
def delete_customer(customer_id:int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /customers/{customer_id}")
    deleted = crud.delete_customer(db = db, customer_id=customer_id)

    if deleted is None:
        logger.warning(f"Delete Failed - customer {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": f"Customer {customer_id} deleted successfully"}

@router.get("/{customer_id}/orders", response_model=List[schemas.orderOut])
def get_customer_orders(customer_id:int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}/orders")
    customer = crud.get_customer(db = db, id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")

    orders = crud.get_customer_orders(db=db, customer_id=customer_id)
    
    return orders

@router.get("/{customer_id}/payments", response_model=List[schemas.paymentOut])
def get_customer_payments(customer_id:int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}/payments")
    customer = crud.get_customer(db = db, id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")

    payments = crud.get_customer_payments(db=db, customer_id=customer_id)
    
    return payments
