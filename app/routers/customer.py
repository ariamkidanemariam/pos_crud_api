from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.customer import CustomerUpdate, CustomerCreate, CustomerRead
from app.services import customer as customer_service
from uuid import UUID
router = APIRouter(prefix="/customer", tags=["Customer"])


@router.get("/", response_model=list[CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return customer_service.list_customers(db)


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: UUID, db: Session = Depends(get_db)):
    return customer_service.get_customer(db, customer_id)


@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db, data)


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: UUID, data: CustomerUpdate, db: Session = Depends(get_db)
):
    return customer_service.update_customer(db, customer_id, data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):
    return customer_service.delete_customer(db, customer_id)
