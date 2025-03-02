from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class ResponseBase(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}  # Default to empty JSON
    latency: float
    token_count: int


# Properties to receive on response creation
class ResponseCreate(ResponseBase):
    prompt_id: UUID
    llm_provider_id: Optional[UUID] = None


# Properties returned in API responses
class ResponseResponse(ResponseBase):
    id: UUID
    prompt_id: UUID
    llm_provider_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
