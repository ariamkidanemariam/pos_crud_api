from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from app.services.auth_service import register, authenticate
from app.schemas.user import UserCreate, UserRead


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return register(db, data)


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return authenticate(
        db,
        form_data.username,
        form_data.password,
    )