from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from logger import get_logger
from database import get_db
import crud
import asyncio
import schemas
import time

logger = get_logger(__name__)

router = APIRouter(tags=["Counter"])

@router.get("/customers/count")
def get_customers_count(db: Session = Depends(get_db)):
    logger.info("GET /customers/count")
    count = crud.get_customers_count(db)
    logger.info(f"Returning customers count = {count}")
    return {"count": count}

@router.get("/orders/count")
def get_orders_count(db: Session = Depends(get_db)):
    logger.info("GET /orders/count")
    count = crud.get_orders_count(db)
    logger.info(f"Returning orders count = {count}")
    return {"count": count}

@router.get("/orderdetails/count")
def get_orderdetails_count(db: Session = Depends(get_db)):
    logger.info("GET /orderdetails/count")
    count = crud.get_orderdetails_count(db)
    logger.info(f"Returning orderdetails count = {count}")
    return {"count": count}

@router.get("/offices/count")
def get_offices_count(db: Session = Depends(get_db)):
    logger.info("GET /offices/count")
    count = crud.get_offices_count(db)
    logger.info(f"Returning offices count = {count}")
    return {"count": count}

@router.get("/employees/count")
def get_employees_count(db: Session = Depends(get_db)):
    logger.info("GET /employees/count")
    count = crud.get_employees_count(db)
    logger.info(f"Returning employees count = {count}")
    return {"count": count}

@router.get("/products/count")
def get_products_count(db: Session = Depends(get_db)):
    logger.info("GET /products/count")
    count = crud.get_products_count(db)
    logger.info(f"Returning products count = {count}")
    return {"count": count}

@router.get("/payments/count")
def get_payments_count(db: Session = Depends(get_db)):
    logger.info("GET /payments/count")
    count = crud.get_payments_count(db)
    logger.info(f"Returning payments count = {count}")
    return {"count": count}

@router.get("/productlines/count")
def get_productlines_count(db: Session = Depends(get_db)):
    logger.info("GET /productlines/count")
    count = crud.get_productlines_count(db)
    logger.info(f"Returning productlines count = {count}")
    return {"count": count}

@router.get("/overall_counts", response_model=schemas.overallCountOut)
async def get_overallCount(db: Session = Depends(get_db)):
    logger.info("GET /overall_count - starting all 8 queries simultaneously")
    startTime = time.time()
    (
    customers,
    orders,
    products,
    employees,
    offices,
    payments,
    orderdetails,
    productlines
    ) = await asyncio.gather(
        asyncio.to_thread(crud.get_customers_count,db),
        asyncio.to_thread(crud.get_orders_count,db),
        asyncio.to_thread(crud.get_products_count,db),
        asyncio.to_thread(crud.get_employees_count,db),
        asyncio.to_thread(crud.get_offices_count,db),
        asyncio.to_thread(crud.get_payments_count,db),
        asyncio.to_thread(crud.get_orderdetails_count,db),
        asyncio.to_thread(crud.get_productlines_count,db)
    )
    endTime = time.time()
    totalTime = round(endTime - startTime, 4)

    logger.info("asyncio.gather() completed all 8 queries")
    logger.info(f"Total response time : {totalTime} seconds")
    return {
        "customers": customers,
        "orders": orders,
        "products": products,
        "employees": employees,
        "offices": offices,
        "payments": payments,
        "orderdetails": orderdetails,
        "productlines": productlines
    }


