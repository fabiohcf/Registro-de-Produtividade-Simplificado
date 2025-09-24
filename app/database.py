# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

# Detecta modo de teste via variável TESTING ou presença do PYTEST_CURRENT_TEST
TESTING = os.getenv("TESTING", "").lower() in ("1", "true", "yes") or (
    "PYTEST_CURRENT_TEST" in os.environ
)

if TESTING:
    # Em testes, usar SQLite em memória por isolamento e performance
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
else:
    # Em execução normal, exigir DATABASE_URL (priorizar PostgreSQL)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL não definido. Ex.: postgresql+psycopg2://usuario:senha@localhost:5432/registro_prod"
        )

# Se estiver em testes (pytest geralmente usa in-memory), força NullPool
if DATABASE_URL.startswith("sqlite:///") and ":memory:" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
        future=True,
    )
else:
    # Para SQLite arquivo, ainda é necessário o check_same_thread=False; para Postgres, sem connect_args
    connect_args = (
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )
    engine = create_engine(
        DATABASE_URL,
        future=True,
        connect_args=connect_args,
        pool_pre_ping=True,
    )

# Sessão principal usada pelos blueprints e testes
db_session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False)
)

# Base para os models
Base = declarative_base()
Base.query = db_session.query_property()


def get_db_session():
    """
    Gerador de sessão para uso como dependência.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    """
    Inicializa o banco criando as tabelas.
    """
    import app.models.user
    import app.models.session
    import app.models.goal

    Base.metadata.create_all(bind=engine)
