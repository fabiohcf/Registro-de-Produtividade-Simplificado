# app/tests/test_api.py

import uuid
from werkzeug.security import generate_password_hash
from app.models.user import User


def test_get_users(client, db_session):
    unique_email = f"{uuid.uuid4()}@example.com"

    # Cria o usuário com hash da senha
    user = User(
        username="Test User API",
        email=unique_email,
        password_hash=generate_password_hash("123456"),
    )
    db_session.add(user)
    db_session.commit()

    # Faz a requisição para listar usuários
    response = client.get("/api/users/")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert any(u["email"] == unique_email for u in data)
