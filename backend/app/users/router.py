from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import current_user
from app.users.schema import UserResponse
from app.users.schema import UserUpdate
from app.users.service import update_user

from app.core.database import get_db
from app.users.schema import UserCreate, UserResponse
from app.users.service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )

    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already taken.",
        )

    return create_user(db, user)

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_profile(
    current=Depends(current_user),
):
    """
    Get current authenticated user's profile.
    """

    return current


@router.put(
    "/me",
    response_model=UserResponse,
)
def update_profile(
    payload: UserUpdate,
    current=Depends(current_user),
    db: Session = Depends(get_db),
):
    return update_user(
        db,
        current,
        payload.model_dump(exclude_unset=True),
    )
