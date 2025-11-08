from sqlalchemy import Column, ForeignKey, DateTime, Numeric, String
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base

class Session(Base):
    __tablename__ = "sessions"

    # UUID para o ID da sessão
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relacionamentos com UUID
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="SET NULL"))

    # Novos campos
    description = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True)

    # Tempo
    duration_hours = Column(Numeric(10, 4), nullable=False, default=0.0)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="sessions")
    goal = relationship("Goal", back_populates="sessions")
