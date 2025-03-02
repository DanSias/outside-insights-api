from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.schemas.llm_provider import LLMProviderCreate, LLMProviderResponse
from app.db.crud.llm_provider import (
    create_llm_provider,
    get_llm_provider,
    list_llm_providers,
)
from app.core.security import get_current_user

router = APIRouter()


@router.post(
    "/", response_model=LLMProviderResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_llm_provider(
    *, db: Session = Depends(get_db), llm_in: LLMProviderCreate
):
    """
    Register a new LLM provider
    """
    return create_llm_provider(db=db, llm_in=llm_in)


@router.get("/{provider_id}", response_model=LLMProviderResponse)
async def get_llm_provider_by_id(*, db: Session = Depends(get_db), provider_id: UUID):
    """
    Get an LLM provider by ID
    """
    provider = get_llm_provider(db, provider_id=provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="LLM Provider not found"
        )
    return provider


@router.get("/", response_model=List[LLMProviderResponse])
async def list_llm_providers(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    List available LLM providers
    """
    return list_llm_providers(db)
