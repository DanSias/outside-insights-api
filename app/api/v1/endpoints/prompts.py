from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.prompt import PromptCreate, PromptResponse, PromptList
from app.schemas.response import ResponseCreate, ResponseRead
from app.db.crud.prompt import (
    create_prompt,
    get_prompt,
    get_prompts_by_user,
    get_prompts_by_organization,
)
from app.services.llm_service import llm_service

router = APIRouter()


@router.post("/", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def submit_prompt(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    prompt_in: PromptCreate,
):
    """
    Submit a prompt to an LLM provider and get a response
    """
    # Create prompt record
    prompt = create_prompt(
        db=db,
        content=prompt_in.content,
        parameters=prompt_in.parameters,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )

    # Process the prompt with the specified LLM provider
    response = await llm_service.process_prompt(
        db=db,
        prompt=prompt,
        provider_name=prompt_in.llm_provider,
        parameters=prompt_in.parameters,
    )

    return {
        "prompt_id": str(prompt.uuid),
        "prompt_content": prompt.content,
        "response_id": str(response.uuid),
        "response_content": response.content,
        "llm_provider": prompt_in.llm_provider,
        "latency": response.latency,
        "token_count": response.token_count,
        "created_at": prompt.created_at,
    }


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt_with_responses(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    prompt_id: str,
):
    """
    Get a specific prompt and its responses
    """
    prompt = get_prompt(db, uuid=prompt_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found"
        )

    # Check if user has access to this prompt
    if prompt.user_id != current_user.id and not current_user.is_superuser:
        if prompt.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this prompt",
            )

    # Get the latest response
    response = prompt.responses[0] if prompt.responses else None

    if not response:
        return {
            "prompt_id": str(prompt.uuid),
            "prompt_content": prompt.content,
            "response_id": None,
            "response_content": None,
            "llm_provider": None,
            "latency": None,
            "token_count": None,
            "created_at": prompt.created_at,
        }

    return {
        "prompt_id": str(prompt.uuid),
        "prompt_content": prompt.content,
        "response_id": str(response.uuid),
        "response_content": response.content,
        "llm_provider": response.llm_provider.name,
        "latency": response.latency,
        "token_count": response.token_count,
        "created_at": prompt.created_at,
    }


@router.get("/", response_model=List[PromptList])
async def list_prompts(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    org_only: bool = False,
):
    """
    List prompts for the current user or organization
    """
    if org_only and not current_user.is_superuser:
        prompts = get_prompts_by_organization(
            db, organization_id=current_user.organization_id, skip=skip, limit=limit
        )
    else:
        prompts = get_prompts_by_user(
            db, user_id=current_user.id, skip=skip, limit=limit
        )

    return [
        {
            "prompt_id": str(p.uuid),
            "content": p.content[:100] + "..." if len(p.content) > 100 else p.content,
            "created_at": p.created_at,
            "response_count": len(p.responses),
        }
        for p in prompts
    ]
