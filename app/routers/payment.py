from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user, require_roles
from app.models.user import UserRole
from app.schemas.payment import PaymentUpdate, PaymentCreate, PaymentRead
from app.services import payment as payment_service

router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[PaymentRead])
def list_payments(db: Session = Depends(get_db)):
    return payment_service.list_payments(db)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: UUID, db: Session = Depends(get_db)):
    return payment_service.get_payment(db, payment_id)


@router.get("/status/{payment_status}", response_model=list[PaymentRead])
def list_payments_by_status(payment_status: str, db: Session = Depends(get_db)):
    return payment_service.list_payments_by_status(db, payment_status)


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db, data)


@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: UUID, data: PaymentUpdate, db: Session = Depends(get_db)):
    return payment_service.update_payment(db, payment_id, data)


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.STORE_MANAGER))],
)
def delete_payment(payment_id: UUID, db: Session = Depends(get_db)):
    return payment_service.delete_payment(db, payment_id)