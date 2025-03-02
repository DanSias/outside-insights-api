from sqlalchemy import Column, String, JSON, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid
import enum


class AuthMethod(enum.Enum):
    API_KEY = "api_key"
    OAUTH = "oauth"


class LLMProvider(Base):
    __tablename__ = "llm_providers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = Column(
        String, unique=True, nullable=False, index=True
    )  # e.g., "OpenAI", "Anthropic", "Cohere"
    api_base_url = Column(String, nullable=False)
    auth_method = Column(Enum(AuthMethod), nullable=False, default=AuthMethod.API_KEY)
    config = Column(JSON, nullable=False, server_default="{}")  # Default to empty JSON

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    responses = relationship(
        "Response", back_populates="llm_provider", cascade="all, delete-orphan"
    )
