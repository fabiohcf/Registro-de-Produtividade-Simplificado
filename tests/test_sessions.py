# tests/test_sessions.py

import uuid
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.session import Session
import pytest

def test_create_session(db_session):
    unique_email = f"{uuid.uuid4()}@example.com"

    # Cria o usuário com senha hash
    user = User(
        username="User Session",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    # Usa datetime timezone-aware consistente com o model
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=1)
    duration_hours = (end_time - start_time).total_seconds() / 3600

    # Cria a sessão
    sessao = Session(
        user_id=user.id,
        started_at=start_time,
        finished_at=end_time,
        duration_hours=duration_hours
    )
    db_session.add(sessao)
    db_session.commit()

    # Valida a sessão criada
    db_sessao = db_session.query(Session).filter_by(user_id=user.id).first()
    assert db_sessao is not None
    assert db_sessao.user_id == user.id

    # Corrige comparação: converte para naive
    assert db_sessao.started_at.replace(tzinfo=None) == start_time.replace(tzinfo=None)
    assert db_sessao.finished_at.replace(tzinfo=None) == end_time.replace(tzinfo=None)
