from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


# Shared properties
class OrganizationBase(BaseModel):
    name: str


# Properties to receive via API on creation
class OrganizationCreate(OrganizationBase):
    pass  # No additional fields needed for now


# Properties received via API on update
class OrganizationUpdate(BaseModel):
    name: Optional[str] = None


# Properties shared by models stored in DB
class OrganizationInDBBase(OrganizationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enables automatic conversion from ORM to Pydantic


# Properties to return to client
class OrganizationResponse(OrganizationInDBBase):
    pass


# Properties stored in DB
class OrganizationInDB(OrganizationInDBBase):
    pass  # No sensitive fields to hide
