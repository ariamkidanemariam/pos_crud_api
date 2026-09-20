from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.category import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate

def get_category(db: Session, category_id: int):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category

def list_categorys(db: Session):
    return category_repository.get_all(db)

def create_category(db: Session, data: CategoryCreate):
    new_category = category_repository.create(db, data.model_dump())
    
    try:
        db.refresh(new_category)
    except Exception:
        db.commit()
    
    return new_category

def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = get_category(db, category_id)
    updated_category = category_repository.update(db, category, data.model_dump(exclude_unset=True))
    db.commit()
    return updated_category

def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    category_repository.delete(db, category)
    db.commit()
