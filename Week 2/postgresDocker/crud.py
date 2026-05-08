from sqlalchemy.orm import Session
import models
import schemas

def get_customers(db: Session, skip: int = 0, limit: int=100):
    print(f"Fetching customers: skip = {skip}, limit ={limit}")
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    print(f"Found {len(customers)} customers")
    return customers

def get_customer(db: Session, id: int):
    print(f"Fetching customer data with id = {id}")
    customer = db.query(models.Customer).filter(models.Customer.customerNumber==id).first()
    if customer is not None:
        print(f"Customer found: {customer.customerName}")
    else:
        print(f"Customer not found: ID {id}")
    return customer


def create_customer(db:Session, customer: schemas.customerCreate):
    print(f"Creating new customer: {customer.customerName}")
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    print("Customer created successfully")

    return new_customer

def update_customer(db:Session, customer_id: int, updates: schemas.customerUpdate):
    print(f"Updating customer ID: {customer_id}")

    db_customer = db.query(models.Customer).filter(models.Customer.customerNumber == customer_id).first()

    if db_customer is None:
        print(f"Update Failed: Customer not found. ID {customer_id}")
        return None

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_customer, field, value)

    db.commit()
    db.refresh(db_customer)
    print(f"Customer ID {customer_id} updated successfully")

    return db_customer

def delete_customer(db:Session, customer_id: int):
    print(f"Deleting customer ID: {customer_id}")

    db_customer = db.query(models.Customer).filter(models.Customer.customerNumber == customer_id).first()

    if db_customer is None:
        print(f"Delete Failed: Customer not found. ID {customer_id}")
        return None
    db.delete(db_customer)
    db.commit()
    print(f"Customer ID {customer_id} deleted successfully")

    return db_customer

def get_customer_orders(db:Session, customer_id: int):
    print(f"Fetching orders of customer ID: {customer_id}")

    orders = db.query(models.Order).filter(models.Order.customerNumber == customer_id).all()

    print(f"Found {len(orders)} orders for customer ID {customer_id}")
    return orders

def get_customer_payments(db:Session, customer_id: int):
    print(f"Fetching payments of customer ID: {customer_id}")

    payments = db.query(models.Payment).filter(models.Payment.customerNumber == customer_id).all()

    print(f"Found {len(payments)} payments for customer ID {customer_id}")
    return payments