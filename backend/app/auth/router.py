from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schema import Token
from app.auth.service import authenticate_user
from app.core.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
    summary="Login with email and password",
    description=(
        "Authenticate a user using their email address "
        "and password. In the OAuth2 form, the email is "
        "submitted through the `username` field."
    ),
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    access_token = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }