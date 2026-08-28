from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

    model_config = ConfigDict(
        extra="forbid"
    )

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)