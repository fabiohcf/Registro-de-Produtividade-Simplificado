# tests/conftest.py

import pytest
import gc
from app import create_app
from app.database import Base, engine, SessionLocal

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()  # Fecha todas as conexões
    gc.collect()      # Força coleta de garbage

@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    app = create_app(testing=True)
    app.config["TESTING"] = True

    # Override da session para testes
    from app import database
    database.SessionLocal = lambda: db_session

    # Contexto completo para teardown
    with app.test_client(use_cookies=True) as client:
        with app.app_context():
            yield client

    # Teardown completo
    app.do_teardown_appcontext()
    engine.dispose()
    gc.collect()

