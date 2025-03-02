# app/models/organization.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = Column(String, unique=True, nullable=False, index=True)
    api_key = Column(
        String, unique=True, nullable=False, index=True
    )  # Consider encrypting before storing

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    users = relationship(
        "User", back_populates="organization", cascade="all, delete-orphan"
    )
    teams = relationship(
        "Team", back_populates="organization", cascade="all, delete-orphan"
    )
