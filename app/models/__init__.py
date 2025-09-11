# app/models/__init__.py

# Importa todos os modelos para o SQLAlchemy reconhecer os mappers
from app.models.user import User
from app.models.goal import Goal
from app.models.session import Session

__all__ = ["User", "Goal", "Session"]
