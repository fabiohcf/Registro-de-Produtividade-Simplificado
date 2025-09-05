# app/models/goal.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String(255), nullable=False)
    type = Column(String(50), nullable=True)
    target_hours = Column(Integer, default=0, nullable=False)

    user = relationship("User", backref="goals")
