# app/models/response.py
from sqlalchemy import Column, Text, ForeignKey, DateTime, JSON, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


class Response(Base):
    __tablename__ = "responses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    content = Column(Text, nullable=False)  # Ensure content is always required
    metadata = Column(
        JSON, nullable=False, server_default="{}"
    )  # Default to empty JSON

    prompt_id = Column(
        UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False
    )
    llm_provider_id = Column(
        UUID(as_uuid=True),
        ForeignKey("llm_providers.id", ondelete="SET NULL"),
        nullable=True,
    )

    latency = Column(Float, default=0.0)  # Default latency to 0.0 seconds
    token_count = Column(Integer, default=0)  # Default token count to 0

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    prompt = relationship("Prompt", back_populates="responses")
    llm_provider = relationship("LLMProvider", back_populates="responses")
