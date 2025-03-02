from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Dict
from enum import Enum


class AuthMethod(str, Enum):
    API_KEY = "api_key"
    OAUTH = "oauth"


class LLMProviderBase(BaseModel):
    name: str
    api_base_url: str
    auth_method: AuthMethod
    config: Dict = {}


class LLMProviderCreate(LLMProviderBase):
    pass


class LLMProviderResponse(LLMProviderBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
