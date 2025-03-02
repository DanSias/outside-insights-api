# app/models/prompt.py
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    content = Column(Text, nullable=False)  # Ensure content is always required
    parameters = Column(
        JSON, nullable=False, server_default="{}"
    )  # JSON defaults to empty object

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="prompts")
    responses = relationship(
        "Response", back_populates="prompt", cascade="all, delete-orphan"
    )
