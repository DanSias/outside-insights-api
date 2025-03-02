from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class PromptBase(BaseModel):
    content: str
    parameters: Dict[str, Any] = {}  # Default to empty dictionary
    llm_provider: str  # Name of the LLM provider used


# Properties to receive on prompt creation
class PromptCreate(PromptBase):
    user_id: UUID
    organization_id: Optional[UUID] = None


# Properties returned in API responses
class PromptResponse(PromptBase):
    id: UUID
    response_id: Optional[UUID] = None
    response_content: Optional[str] = None
    latency: Optional[float] = None
    token_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties for listing prompts
class PromptList(PromptBase):
    id: UUID
    created_at: datetime
    response_count: int

    class Config:
        orm_mode = True
