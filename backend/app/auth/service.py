from datetime import timedelta

from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    verify_password,
)
from app.users.service import get_user_by_email


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    """
    Authenticate user and return JWT token.
    """
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return access_token


def get_current_user(
    db: Session,
    token: str,
):
    """
    Retrieve the current authenticated user from a JWT.
    """
    payload = decode_access_token(token)

    if payload is None:
        return None

    email = payload.get("sub")

    if email is None:
        return None

    return get_user_by_email(db, email)