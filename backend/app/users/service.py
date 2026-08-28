from sqlalchemy.orm import Session

from app.users.model import User
from app.users.schema import UserCreate
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    """
    Find a user by email.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """
    Find a user by username.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user.
    """

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
    
def update_user(
    db: Session,
    user: User,
    update_data: dict,
):
    """
    Update current user.
    """

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()

    db.refresh(user)

    return user