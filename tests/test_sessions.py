# tests/test_sessions.py

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.session import Session
from app.models.goal import Goal
from app.database import SessionLocal
import pytest


@pytest.fixture
def test_user():
    """Cria e retorna um usuário de teste com UUID"""
    with SessionLocal() as db:
        user = User(
            username=f"User_{uuid.uuid4()}",
            email=f"{uuid.uuid4()}@example.com",
            password_hash=generate_password_hash("123456"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        yield user
        db.delete(user)
        db.commit()


@pytest.fixture
def test_goal(test_user):
    """Cria e retorna uma meta de teste para o usuário"""
    with SessionLocal() as db:
        goal = Goal(
            user_id=test_user.id,
            description="Meta de teste",
            category="study",
            target_hours=10.0,
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        yield goal
        db.delete(goal)
        db.commit()


def test_create_session_db(test_user):
    """Testa criação direta de sessão no banco"""
    with SessionLocal() as db:
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=2)
        duration = (end_time - start_time).total_seconds() / 3600

        session_obj = Session(
            user_id=test_user.id,
            started_at=start_time,
            finished_at=end_time,
            duration_hours=Decimal(duration),
        )
        db.add(session_obj)
        db.commit()
        db.refresh(session_obj)

        assert session_obj.id is not None
        assert session_obj.user_id == test_user.id
        assert abs(float(session_obj.duration_hours) - duration) < 1e-6


def test_start_pause_finish_session(client, test_user):
    """Testa endpoints de sessão (start, pause, restart, finish)"""
    user_uuid = str(test_user.id)

    # Start
    resp = client.post("/api/sessions/start", json={"user_id": user_uuid})
    assert resp.status_code == 201
    session_id = resp.get_json()["session_id"]

    # Pause
    resp = client.post("/api/sessions/pause", json={"session_id": session_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "duration_hours" in data

    # Restart
    resp = client.post("/api/sessions/restart", json={"session_id": session_id})
    assert resp.status_code == 200

    # Finish
    resp = client.post("/api/sessions/finish", json={"session_id": session_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "duration_hours" in data


def test_frontend_finish_session(client, test_user):
    """Testa endpoint /frontend_finish"""
    user_uuid = str(test_user.id)
    now_seconds = 3600  # 1 hora

    payload = {
        "user_id": user_uuid,
        "description": "Sessão do frontend",
        "type": "Estudo",
        "netTime": now_seconds,
        "grossTime": now_seconds,
    }

    resp = client.post("/api/sessions/frontend_finish", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "session_id" in data
    assert isinstance(data["session_id"], str)
