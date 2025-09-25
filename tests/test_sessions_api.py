# tests/test_sessions_api.py
from decimal import Decimal
import uuid
import pytest
from datetime import datetime, timezone
from app.models.user import User
from app.models.session import Session
from app.models.goal import Goal
from werkzeug.security import generate_password_hash


@pytest.fixture
def test_user(db_session):
    """Cria um usuário de teste"""
    user = User(
        username="API User",
        email=f"{uuid.uuid4()}@example.com",
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_goal(db_session, test_user):
    """Cria uma meta de teste"""
    goal = Goal(
        user_id=test_user.id,
        category="Meta de teste",
        description="Descrição da meta",
        target_hours=5
    )
    db_session.add(goal)
    db_session.commit()
    return goal


def test_start_pause_restart_finish_session(client, db_session, test_user, test_goal):
    """Testa fluxo completo de sessão via API"""
    resp = client.post("/api/sessions/start", json={"user_id": test_user.id})
    assert resp.status_code == 201
    session_id = resp.get_json()["session_id"]

    resp = client.post("/api/sessions/pause", json={"session_id": session_id})
    assert resp.status_code == 200
    duration1 = Decimal(str(resp.get_json()["duration_hours"]))
    assert duration1 >= Decimal("0.0000")

    resp = client.post("/api/sessions/restart", json={"session_id": session_id})
    assert resp.status_code == 200

    resp = client.post("/api/sessions/finish", json={"session_id": session_id})
    assert resp.status_code == 200
    duration2 = Decimal(str(resp.get_json()["duration_hours"]))
    assert duration2 >= Decimal("0.0000")


def test_start_session_with_goal(client, db_session, test_user, test_goal):
    """Inicia sessão já associada a uma meta"""
    resp = client.post("/api/sessions/start", json={
        "user_id": test_user.id,
        "goal_id": test_goal.id
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["goal_id"] == test_goal.id


def test_set_session_goal(client, db_session, test_user, test_goal):
    """Associa meta a uma sessão existente"""
    session = Session(
        user_id=test_user.id,
        started_at=datetime.now(timezone.utc),
        duration_hours=Decimal("0.0000")
    )
    db_session.add(session)
    db_session.commit()

    resp = client.post("/api/sessions/set_goal", json={
        "session_id": session.id,
        "goal_id": test_goal.id
    })
    assert resp.status_code == 200
    db_session.refresh(session)
    assert session.goal_id == test_goal.id


def test_invalid_inputs(client, db_session):
    """Testa validações de input e erros"""
    resp = client.post("/api/sessions/start", json={})
    assert resp.status_code == 400

    resp = client.post("/api/sessions/pause", json={"session_id": 999999})
    assert resp.status_code == 404

    resp = client.post("/api/sessions/set_goal", json={"session_id": 999999, "goal_id": 1})
    assert resp.status_code == 404

    resp = client.post("/api/sessions/set_goal", json={"session_id": 1, "goal_id": 999999})
    assert resp.status_code in (400, 404)


def test_pause_finished_session(client, db_session, test_user):
    """Tenta pausar sessão que já foi finalizada"""
    session = Session(
        user_id=test_user.id,
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
        duration_hours=Decimal("1.0000")
    )
    db_session.add(session)
    db_session.commit()

    resp = client.post("/api/sessions/pause", json={"session_id": session.id})
    assert resp.status_code == 400


def test_restart_nonexistent_session(client):
    """Tenta reiniciar sessão inexistente"""
    resp = client.post("/api/sessions/restart", json={"session_id": 999999})
    assert resp.status_code == 404


def test_finish_without_start(client, db_session, test_user):
    """Tenta finalizar sessão sem ter iniciado corretamente"""
    session = Session(
        user_id=test_user.id,
        started_at=None,
        finished_at=None,
        duration_hours=Decimal("0.0000")
    )
    db_session.add(session)
    db_session.commit()

    resp = client.post("/api/sessions/finish", json={"session_id": session.id})
    assert resp.status_code in (400, 500)
