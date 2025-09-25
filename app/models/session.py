# app/models/session.py

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="SET NULL"))
    # precisão de horas com 4 casas decimais
    duration_hours = Column(Numeric(10, 4), nullable=False, default=0.0)

    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="sessions")
    goal = relationship("Goal", back_populates="sessions")
