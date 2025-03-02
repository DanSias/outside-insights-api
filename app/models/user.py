from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    organization = relationship("Organization", back_populates="users")
    teams = relationship(
        "TeamMember", back_populates="user", cascade="all, delete-orphan"
    )
    prompts = relationship(
        "Prompt", back_populates="user", cascade="all, delete-orphan"
    )
