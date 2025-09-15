# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Se estivermos em testes, força NullPool para SQLite in-memory
if DATABASE_URL == "sqlite:///:memory:":
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=NullPool, future=True)
else:
    engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db_session():
    """
    Cria e retorna uma sessão de banco para uso via dependência.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
