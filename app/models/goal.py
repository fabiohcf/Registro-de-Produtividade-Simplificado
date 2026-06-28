# app/models/goal.py

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Numeric,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Goal(Base):
    __tablename__ = "goals"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "year",
            "week_number",
            name="uq_goal_user_week"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Meta semanal de horas (opcional)
    target_hours = Column(
        Numeric(10, 2),
        nullable=True
    )

    # Meta semanal de questões (opcional)
    target_questions = Column(
        Integer,
        nullable=True
    )

    # Ano da semana ISO
    year = Column(
        Integer,
        nullable=False
    )

    # Semana ISO (1–53)
    week_number = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="goals"
    )

    sessions = relationship(
        "Session",
        back_populates="goal"
    )