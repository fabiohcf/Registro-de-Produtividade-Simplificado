# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

# Detecta modo de teste
TESTING = os.getenv("TESTING", "").lower() in ("1", "true", "yes") or (
    "PYTEST_CURRENT_TEST" in os.environ
)

# Define URL do banco
if TESTING:
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL não definido. Ex.: postgresql+psycopg2://usuario:senha@localhost:5432/registro_prod"
        )

# Configuração do engine
if DATABASE_URL.startswith("sqlite") and ":memory:" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
        future=True,
    )
else:
    connect_args = (
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )

    engine = create_engine(
        DATABASE_URL,
        future=True,
        connect_args=connect_args,
        pool_pre_ping=True,
    )

# Base dos models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Scoped session para uso global
db_session = scoped_session(SessionLocal)

Base.query = db_session.query_property()


def get_db_session():
    """
    Gerador de sessão para dependências (ex: rotas ou serviços).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco criando as tabelas.
    """
    import app.models.user
    import app.models.session
    import app.models.goal

    Base.metadata.create_all(bind=engine)