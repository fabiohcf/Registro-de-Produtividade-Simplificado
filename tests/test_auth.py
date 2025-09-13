# tests/test_auth.py

import json
import uuid
import pytest
from werkzeug.security import generate_password_hash
from app.models.user import User
from app import create_app
from app.database import Base, engine, sessionmaker

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_login_endpoint(client, db_session):
    # Cria usuário
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(
        username="Test User",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    # Faz login
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "Test User", "password": "123456"}),
        content_type="application/json"
    )
    data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data

def test_refresh_endpoint(client, db_session):
    # Cria usuário
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(
        username="Test User 2",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    # Login para pegar refresh token
    login_resp = client.post(
        "/auth/login",
        data=json.dumps({"username": "Test User 2", "password": "123456"}),
        content_type="application/json"
    )
    refresh_token = login_resp.get_json()["refresh_token"]

    # Usa refresh token para gerar novo access token
    response = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in data
