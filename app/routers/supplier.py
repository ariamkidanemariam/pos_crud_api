from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user, require_roles
from app.models.user import UserRole
from app.schemas.supplier import SupplierUpdate, SupplierCreate, SupplierRead
from app.services import supplier as supplier_service

router = APIRouter(
    prefix="/supplier",
    tags=["Supplier"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/", response_model=list[SupplierRead])
def list_suppliers(db: Session = Depends(get_db)):
    return supplier_service.list_suppliers(db)

@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: UUID, db: Session = Depends(get_db)):
    return supplier_service.get_supplier(db, supplier_id)

@router.post("/", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    return supplier_service.create_supplier(db, data)

@router.put("/{supplier_id}", response_model=SupplierRead)
def update_supplier(supplier_id: UUID, data: SupplierUpdate, db: Session = Depends(get_db)):
    return supplier_service.update_supplier(db, supplier_id, data)

@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.STORE_MANAGER))],
)
def delete_supplier(supplier_id: UUID, db: Session = Depends(get_db)):
    return supplier_service.delete_supplier(db, supplier_id)