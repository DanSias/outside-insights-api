from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None  # Added for job titles
    is_active: Optional[bool] = True
    is_superuser: bool = False
    organization_id: Optional[UUID] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    organization_id: Optional[UUID] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Properties to return to client
class UserResponse(UserInDBBase):
    pass


# Properties stored in DB (password should not be exposed)
class UserInDB(UserInDBBase):
    hashed_password: str
