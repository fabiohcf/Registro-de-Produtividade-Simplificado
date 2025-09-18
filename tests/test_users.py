# app/tests/test_users.py

import uuid
from werkzeug.security import generate_password_hash
from app.models.user import User

def test_create_user(client, db_session):
    unique_email = f"{uuid.uuid4()}@example.com"

    # Dados para criar usuário via API (rota ainda recebe "password")
    user_data = {
        "username": "Test User",
        "email": unique_email,
        "password": "123456"
    }

    # Envia POST para criar usuário
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 201

    # Valida que o usuário foi criado no banco
    db_user = db_session.query(User).filter_by(email=unique_email).first()
    assert db_user is not None
    assert db_user.username == "Test User"
    assert db_user.password_hash != "123456"  # garante que a senha foi hasheada corretamente
