from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.supplier import supplier_repository
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.models.supplier import Supplier

def get_supplier(db: Session, supplier_id: str):
    supplier = supplier_repository.get(db, supplier_id) 
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
        )
    return supplier

def list_suppliers(db: Session):
    return supplier_repository.get_all(db)

def create_supplier(db: Session, data: SupplierCreate):
    try:
        return supplier_repository.create(db, data.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A supplier with this email address already exists."
        )

def update_supplier(db: Session, supplier_id: str, data: SupplierUpdate):
    supplier = get_supplier(db, supplier_id)
    try:
        return supplier_repository.update(db, supplier, data.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The updated email is already taken by another supplier."
        )

def delete_supplier(db: Session, supplier_id: str):
    supplier = get_supplier(db, supplier_id)
    supplier_repository.delete(db, supplier)
