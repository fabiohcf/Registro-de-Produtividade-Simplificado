# app/models/user.py

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base, SessionLocal
import uuid
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    # ID como UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

    @staticmethod
    def get_by_username(username: str):
        with SessionLocal() as session:
            return session.query(User).filter_by(username=username).first()
