from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.team import TeamCreate, TeamResponse
from app.db.crud.team import (
    create_team,
    get_team,
    list_teams_by_organization,
    delete_team,
)

router = APIRouter()


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_new_team(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    team_in: TeamCreate
):
    """
    Create a new team within the current user's organization
    """
    return create_team(
        db=db, team_in=team_in, organization_id=current_user.organization_id
    )


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team_by_id(*, db: Session = Depends(get_db), team_id: UUID):
    """
    Get a team by ID
    """
    team = get_team(db, team_id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    List teams within the current user's organization
    """
    return list_teams_by_organization(db, organization_id=current_user.organization_id)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team(*, db: Session = Depends(get_db), team_id: UUID):
    """
    Delete a team by ID
    """
    delete_team(db, team_id=team_id)
    return None
