from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid
import enum


class Team(Base):
    __tablename__ = "teams"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = Column(String, unique=True, nullable=False)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    organization = relationship("Organization", back_populates="teams")
    members = relationship(
        "TeamMember", back_populates="team", cascade="all, delete-orphan"
    )


class TeamRole(enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    team_id = Column(
        UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(Enum(TeamRole), default=TeamRole.MEMBER)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")
