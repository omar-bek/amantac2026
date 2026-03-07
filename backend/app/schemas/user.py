"""
User schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    full_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True





