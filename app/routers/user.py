from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import require_roles
from app.models.user import UserRole
from app.schemas.user import UserUpdate, UserCreate, UserRead
from app.services import user as user_service

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(require_roles(UserRole.STORE_MANAGER))],
)


@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID, data: UserUpdate, db: Session = Depends(get_db)
):
    return user_service.update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)