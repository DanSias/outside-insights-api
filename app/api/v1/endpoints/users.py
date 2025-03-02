from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.db.crud.user import (
    create_user,
    get_user,
    get_users_by_organization,
    update_user,
    delete_user,
)

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(*, db: Session = Depends(get_db), user_in: UserCreate):
    """
    Create a new user
    """
    user = create_user(db=db, user_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(*, db: Session = Depends(get_db), user_id: UUID):
    """
    Get a user by ID
    """
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    List users in the current user's organization
    """
    users = get_users_by_organization(db, organization_id=current_user.organization_id)
    return users


@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    *, db: Session = Depends(get_db), user_id: UUID, user_in: UserCreate
):
    """
    Update user details
    """
    user = update_user(db, user_id=user_id, user_in=user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(*, db: Session = Depends(get_db), user_id: UUID):
    """
    Delete a user by ID
    """
    delete_user(db, user_id=user_id)
    return None
