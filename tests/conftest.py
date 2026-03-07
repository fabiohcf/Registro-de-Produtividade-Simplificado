# tests/conftest.py

import pytest
from app import create_app
from app.database import Base, engine, SessionLocal


@pytest.fixture(scope="session")
def app():
    """Cria a aplicação Flask para testes."""
    app = create_app(testing=True)
    app.config["TESTING"] = True
    return app


@pytest.fixture(scope="session")
def setup_database():
    """Cria o schema do banco para os testes."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_database):
    """Cria uma sessão isolada para cada teste."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(app, db_session):
    """Cliente HTTP para testes."""
    
    from app import database

    # override da sessão
    database.SessionLocal = lambda: db_session

    with app.test_client(use_cookies=True) as client:
        with app.app_context():
            yield client