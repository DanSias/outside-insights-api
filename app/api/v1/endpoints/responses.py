from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.schemas.response import ResponseResponse
from app.db.crud.response import get_response

router = APIRouter()


@router.get("/{response_id}", response_model=ResponseResponse)
async def get_response_by_id(*, db: Session = Depends(get_db), response_id: UUID):
    """
    Get a response by ID
    """
    response = get_response(db, response_id=response_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Response not found"
        )
    return response
