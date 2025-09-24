# tests/test_users_api.py

import uuid
import git
from werkzeug.security import generate_password_hash
from app.models.user import User


@pytest.mark.parametrize(
    "username,email,password",
    [
        ("Test User 1", f"{uuid.uuid4()}@example.com", "123456"),
        ("Test User 2", f"{uuid.uuid4()}@example.com", "abcdef"),
    ],
)
def test_create_user(client, db_session, username, email, password):
    """Testa criação de usuário via endpoint POST /api/users/"""
    resp = client.post(
        "/api/users/",
        json={"username": username, "email": email, "password": password},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "user_id" in data

    # Confirma no banco
    user = db_session.query(User).filter_by(id=data["user_id"]).first()
    assert user is not None
    assert user.username == username
    assert user.email == email


def test_list_users(client, db_session):
    """Testa listagem de usuários via GET /api/users/"""
    resp = client.get("/api/users/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert all("id" in u and "username" in u and "email" in u for u in data)


def test_get_user_by_id(client, db_session):
    """Testa busca de usuário por ID via GET /api/users/<id>"""
    # Cria usuário manualmente
    user = User(
        username="Fetch User",
        email=f"{uuid.uuid4()}@example.com",
        password_hash=generate_password_hash("123456"),
    )
    db_session.add(user)
    db_session.commit()

    resp = client.get(f"/api/users/{user.id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == user.id
    assert data["username"] == user.username

    # Testa usuário inexistente
    resp = client.get("/api/users/999999")
    assert resp.status_code == 404


def test_update_user(client, db_session):
    """Testa atualização de usuário via PUT /api/users/<id>"""
    user = User(
        username="Old Name",
        email=f"{uuid.uuid4()}@example.com",
        password_hash=generate_password_hash("123456"),
    )
    db_session.add(user)
    db_session.commit()

    resp = client.put(f"/api/users/{user.id}", json={"username": "New Name"})
    assert resp.status_code == 200
    db_session.refresh(user)
    assert user.username == "New Name"


def test_delete_user(client, db_session):
    """Testa exclusão de usuário via DELETE /api/users/<id>"""
    user = User(
        username="To Delete",
        email=f"{uuid.uuid4()}@example.com",
        password_hash=generate_password_hash("123456"),
    )
    db_session.add(user)
    db_session.commit()

    resp = client.delete(f"/api/users/{user.id}")
    assert resp.status_code == 200
    # Confirma remoção do banco
    deleted = db_session.query(User).filter_by(id=user.id).first()
    assert deleted is None
