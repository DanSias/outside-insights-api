from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    organization_id: UUID


class TeamResponse(TeamBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
