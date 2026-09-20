from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.user import UserRole
from dependencies import get_current_user, require_roles

from database import get_db
from app.schemas.product import ProductUpdate, ProductCreate, ProductRead
from app.services import product as product_service

router = APIRouter(prefix="/product", tags=["Product"],
                   dependencies=[Depends(get_current_user)],)

@router.get("/", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return product_service.list_products(db)

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: UUID, db: Session = Depends(get_db)):  
    return product_service.get_product(db, product_id)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, data)

@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: UUID, data: ProductUpdate, db: Session = Depends(get_db)  
):
    return product_service.update_product(db, product_id, data)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.STORE_MANAGER))],
)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)