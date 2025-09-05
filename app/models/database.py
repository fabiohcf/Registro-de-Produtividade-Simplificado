# app/models/database.py 

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Base para os models
Base = declarative_base()

# Engine - conexão com o banco
# Por padrão, vamos usar SQLite local
DATABASE_URL = "sqlite:///app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necessário apenas para SQLite
    echo=False  # Coloque True se quiser ver os SQLs gerados
)

# Factory de sessões
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
