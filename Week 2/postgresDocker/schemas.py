from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal

class orderDetails(BaseModel):
    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: Decimal
    orderLineNumber: int

    class Config:
        from_attributes = True

class orderOut(BaseModel):
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str
    comments: Optional[str]
    customerNumber: int

    class Config:
        from_attributes = True

class paymentOut(BaseModel):
    customerNumber: int
    checkNumber: str
    paymentDate: date
    amount: Decimal

    class Config:
        from_attributes = True


class customerCreate(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName:str
    contactFirstName:str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

class customerOut(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName:str
    contactFirstName:str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None
    orders: List[orderOut] = []
    payments: List[paymentOut] = []


    class Config:
        from_attributes = True

class customerUpdate(BaseModel):
    customerName: Optional[str] = None
    contactLastName:Optional[str] = None
    contactFirstName:Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

print("Schemas Loaded successfully")