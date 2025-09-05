# app/tests/test_auth.py

import uuid
from app.models.user import User
from werkzeug.security import generate_password_hash

def test_login(client, db_session):
    # Cria usuário para teste
    unique_email = f"{uuid.uuid4()}@example.com"
    password = "123456"
    user = User(username="Test Login", email=unique_email, password=generate_password_hash(password))
    db_session.add(user)
    db_session.commit()

    # Faz login via endpoint
    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": password
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data

def test_logout(client):
    # Simula logout usando POST
    response = client.post("/auth/logout")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Logout realizado com sucesso"
