# tests/test_sessions.py

import uuid
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.session import Session
from app.database import SessionLocal
import pytest


def test_create_session():
    session = SessionLocal()

    try:
        # Cria usuário único
        unique_email = f"{uuid.uuid4()}@example.com"
        user = User(
            username="User Session",
            email=unique_email,
            password_hash=generate_password_hash("123456"),
        )
        session.add(user)
        session.commit()

        # Cria sessão com tempos UTC
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=1)
        duration_hours = (end_time - start_time).total_seconds() / 3600

        sessao = Session(
            user_id=user.id,
            started_at=start_time,
            finished_at=end_time,
            duration_hours=duration_hours,
        )
        session.add(sessao)
        session.commit()

        # Busca do banco
        db_sessao = session.query(Session).filter_by(user_id=user.id).first()
        assert db_sessao is not None
        assert db_sessao.user_id == user.id

        # Comparação UTC
        assert db_sessao.started_at.astimezone(timezone.utc) == start_time
        assert db_sessao.finished_at.astimezone(timezone.utc) == end_time
        assert abs(float(db_sessao.duration_hours) - duration_hours) < 1e-6

    finally:
        session.close()


def test_start_pause_finish_session(client):
    # Cria usuário para o teste
    session = SessionLocal()
    try:
        unique_email = f"{uuid.uuid4()}@example.com"
        user = User(
            username="User API",
            email=unique_email,
            password_hash=generate_password_hash("123456"),
        )
        session.add(user)
        session.commit()
        user_id = user.id
    finally:
        session.close()

    # Inicia sessão
    resp = client.post("/api/sessions/start", json={"user_id": user_id})
    assert resp.status_code == 201
    session_id = resp.get_json()["session_id"]

    # Pausa sessão
    resp = client.post("/api/sessions/pause", json={"session_id": session_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "duration_hours" in data

    # Reinicia sessão
    resp = client.post("/api/sessions/restart", json={"session_id": session_id})
    assert resp.status_code == 200

    # Finaliza sessão
    resp = client.post("/api/sessions/finish", json={"session_id": session_id})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "duration_hours" in data
