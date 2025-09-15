# tests/conftest.py

import pytest
from app import create_app
from app.database import Base, engine, SessionLocal

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Cria uma sessão de banco para cada teste."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    """Cria um cliente de teste com cookies habilitados e DB injetado."""
    app = create_app()
    app.config["TESTING"] = True

    # Substitui SessionLocal do app pela sessão de teste
    from app import database
    database.SessionLocal = lambda: db_session

    # Cria o client com cookies habilitados
    with app.test_client(use_cookies=True) as client:
        yield client
