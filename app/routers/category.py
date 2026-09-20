from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.category import CategoryUpdate, CategoryCreate, CategoryRead
from app.services import category as category_service
from uuid import UUID

router=APIRouter(prefix="/category", tags=["Category"])


@router.get("/", response_model=list[CategoryRead])
def list_category(db:Session = Depends (get_db)):
    return category_service.list_categorys(db)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id:UUID, db: Session = Depends(get_db)):
    return category_service.get_category(db, category_id)

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data:CategoryCreate, db: Session=Depends(get_db)):
    return category_service.create_category(db, data)

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: UUID, data: CategoryUpdate, db:Session= Depends(get_db)
):
    return category_service.update_category(db, category_id, data)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    return category_service.delete_category(db, category_id)

