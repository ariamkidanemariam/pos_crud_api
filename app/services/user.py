from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate

from sqlalchemy.exc import IntegrityError

def get_user(db: Session, user_id: str):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

def list_users(db: Session):
    return user_repository.get_all(db) 

def create_user(db: Session, data: UserCreate):
    user_data = data.model_dump()
     
    try:
        return user_repository.create(db, user_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )


def update_user(db: Session, user_id: str, data: UserUpdate):
    user = get_user(db, user_id)
    return user_repository.update(db, user, data.model_dump(exclude_unset=True))

def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    user_repository.delete(db, user)
