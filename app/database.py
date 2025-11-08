# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

TESTING = (
    os.getenv("TESTING", "").lower() in ("1", "true", "yes")
    or "PYTEST_CURRENT_TEST" in os.environ
)

if TESTING:
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")

if DATABASE_URL.startswith("sqlite:///") and ":memory:" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
        future=True,
    )
else:
    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    engine = create_engine(
        DATABASE_URL,
        future=True,
        connect_args=connect_args,
        pool_pre_ping=True,
    )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
db_session = scoped_session(SessionLocal)

Base = declarative_base()
Base.query = db_session.query_property()


def get_db_session():
    """Retorna uma sessão do banco (uso interno Flask, não como dependência)."""
    return db_session()


def init_db():
    """Cria as tabelas do banco."""
    from app.models import user, session  # noqa
    Base.metadata.create_all(bind=engine)
