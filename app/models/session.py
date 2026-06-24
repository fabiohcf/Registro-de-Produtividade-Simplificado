# app/models/session.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String
from sqlalchemy.orm import relationship
from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="SET NULL"))

    duration_hours = Column(Numeric(10, 4), nullable=False, default=0.0)

    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    # V2 fields
    status = Column(String(20), nullable=False, default="running")

    session_type = Column(String(20), nullable=False)
    description = Column(String(255), nullable=True)

    paused_seconds = Column(Integer, nullable=False, default=0)
    paused_at = Column(DateTime(timezone=True), nullable=True)

    questions_total = Column(Integer, nullable=True)
    questions_correct = Column(Integer, nullable=True)

    user = relationship("User", back_populates="sessions")
    goal = relationship("Goal", back_populates="sessions")