from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Dict


class WorkflowBase(BaseModel):
    name: str
    steps: List[Dict]  # JSON-structured steps


class WorkflowResponse(WorkflowBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
