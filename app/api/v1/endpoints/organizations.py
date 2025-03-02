from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.db.crud.organization import (
    create_organization,
    get_organization,
    list_organizations,
    delete_organization,
)
from app.core.security import get_current_user

router = APIRouter()


@router.post(
    "/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_organization(
    *, db: Session = Depends(get_db), org_in: OrganizationCreate
):
    """
    Create a new organization
    """
    return create_organization(db=db, org_in=org_in)


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization_by_id(*, db: Session = Depends(get_db), org_id: UUID):
    """
    Get an organization by ID
    """
    org = get_organization(db, org_id=org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )
    return org


@router.get("/", response_model=List[OrganizationResponse])
async def get_all_organizations(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    List all organizations (admin only)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    return list_organizations(db)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_organization(*, db: Session = Depends(get_db), org_id: UUID):
    """
    Delete an organization by ID
    """
    delete_organization(db, org_id=org_id)
    return None
