from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class FeedbackBase(BaseModel):
    response_id: UUID
    rating: int  # 1-5
    comment: Optional[str] = None


class FeedbackResponse(FeedbackBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
