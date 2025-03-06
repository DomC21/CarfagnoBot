from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user model with common attributes."""
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """User creation model with password."""
    password: str = Field(..., min_length=8)


class UserInDB(UserBase):
    """User model as stored in the database."""
    id: int
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None


class User(UserBase):
    """User model returned to clients (without sensitive data)."""
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT token payload data."""
    email: Optional[str] = None
    exp: Optional[datetime] = None
