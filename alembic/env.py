#alembic/env.py

from logging.config import fileConfig
import os
from dotenv import load_dotenv

from sqlalchemy import engine_from_config, pool
from alembic import context

# Carregar variáveis do .env
load_dotenv()  

# Importar Base do SQLAlchemy e models
from app.database import Base
from app.models import *

# MetaData do projeto, necessária para autogenerate
target_metadata = Base.metadata

# Configuração do Alembic
config = context.config

# Configuração do logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definir a URL do banco pelo .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


def run_migrations_offline() -> None:
    """Executa migrações em modo offline (apenas SQL, sem conexão direta)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações em modo online (com conexão ativa)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
