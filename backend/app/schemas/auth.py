from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, PyEnum):
    Creator = "Creator"
    Reviewer = "Reviewer"
    Admin = "Admin"


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1)
    role: UserRole = UserRole.Creator


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
