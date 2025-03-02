from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    response_id = Column(
        UUID(as_uuid=True),
        ForeignKey("responses.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(Text, nullable=True)  # Optional user feedback
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    response = relationship("Response", back_populates="feedback")
    user = relationship("User")
