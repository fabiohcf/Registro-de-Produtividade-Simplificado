# app/models/goal.py

from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from app.models.base import Base

class Goal(Base):
    __tablename__ = "goals"

    # ID como UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Relacionamento com usuário usando UUID
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    description = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # e.g., study, work, etc.
    target_hours = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="goals")
    sessions = relationship("Session", back_populates="goal", cascade="all, delete-orphan")
