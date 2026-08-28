from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.core.database import get_db
from app.core.security import oauth2_scheme


def current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = get_current_user(db, token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )

    return user