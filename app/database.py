# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Se estivermos em testes, força NullPool para SQLite in-memory
if DATABASE_URL == "sqlite:///:memory:":
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
        future=True
    )
else:
    engine = create_engine(DATABASE_URL, future=True)

# Sessão principal usada pelos blueprints e testes
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

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

# Para compatibilidade com seu código existente
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    """
    Inicializa o banco criando as tabelas.
    """
    import app.models.user
    import app.models.session
    import app.models.goal
    Base.metadata.create_all(bind=engine)
