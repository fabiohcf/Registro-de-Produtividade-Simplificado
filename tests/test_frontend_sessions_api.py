# tests/test_frontend_sessions_api.py
import uuid
from decimal import Decimal
import pytest
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.session import Session


@pytest.fixture
def test_user(db_session):
    """Cria um usuário de teste"""
    user = User(
        username="Frontend User",
        email=f"{uuid.uuid4()}@example.com",
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_frontend_finish_session_success(client, db_session, test_user):
    """Testa criação de sessão via endpoint frontend_finish"""
    payload = {
        "user_id": str(test_user.id),
        "description": "Sessão de teste do frontend",
        "type": "Estudo",
        "netTime": 3600,
        "grossTime": 3700
    }

    resp = client.post("/api/sessions/frontend_finish", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "session_id" in data

    # Verifica no banco
    session = db_session.query(Session).filter_by(id=data["session_id"]).first()
    assert session is not None
    assert session.user_id == test_user.id
    assert session.description == payload["description"]
    assert session.type == payload["type"]
    assert abs(float(session.duration_hours) - Decimal(payload["netTime"]) / 3600) < 1e-6


@pytest.mark.parametrize(
    "payload,error_field",
    [
        ({"user_id": str(uuid.uuid4()), "description": "Teste", "type": "Estudo", "netTime": 3600, "grossTime": 3600}, "Usuário"),
        ({"user_id": "", "description": "Teste", "type": "Estudo", "netTime": 3600, "grossTime": 3600}, "UUID"),
        ({"user_id": str(uuid.uuid4()), "description": "Teste", "netTime": 3600, "grossTime": 3600}, "type"),
        ({"user_id": str(uuid.uuid4()), "description": "Teste", "type": "Estudo"}, "netTime")
    ]
)
def test_frontend_finish_session_errors(client, payload, error_field):
    """Testa casos de erro no endpoint frontend_finish"""
    resp = client.post("/api/sessions/frontend_finish", json=payload)
    assert resp.status_code in (400, 404)
    data = resp.get_json()
    assert error_field.lower() in data.get("error", "").lower()
