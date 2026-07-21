from datetime import datetime, timezone
import uuid
import pytest
from werkzeug.security import generate_password_hash
from decimal import Decimal
from app.models.session import Session
from app.models.goal import Goal
from app.models.user import User


# ==========================================================
# Fixtures
# ==========================================================

@pytest.fixture
def test_user(db_session):
    """Cria um usuário de teste."""

    unique = uuid.uuid4().hex

    user = User(
        username=f"api-user-{unique}",
        email=f"{unique}@test.com",
        password_hash=generate_password_hash("123456"),
    )

    db_session.add(user)
    db_session.commit()

    return user


@pytest.fixture
def weekly_goal(db_session, test_user):
    """Cria uma meta semanal válida para a semana atual."""

    year, week, _ = datetime.now(timezone.utc).isocalendar()

    goal = Goal(
        user_id=test_user.id,
        year=year,
        week_number=week,
        target_hours=10,
        target_questions=300,
    )

    db_session.add(goal)
    db_session.commit()

    return goal


# ==========================================================
# START SESSION
# ==========================================================

def test_start_session_success(client, test_user):

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "session_type": "study",
        },
    )

    assert response.status_code == 201

    body = response.get_json()

    assert body["message"] == "Sessão iniciada com sucesso"

    session = body["session"]

    assert session["status"] == "running"
    assert session["session_type"] == "study"
    assert session["goal_id"] is None
    assert session["questions_total"] is None
    assert session["questions_correct"] is None


def test_start_session_with_description(client, test_user):

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "session_type": "revision",
            "description": " Revisão de Direito Constitucional ",
        },
    )

    assert response.status_code == 201

    session = response.get_json()["session"]

    assert session["description"] == "Revisão de Direito Constitucional"


def test_start_session_with_goal(client, test_user, weekly_goal):

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "session_type": "questions",
            "goal_id": weekly_goal.id,
        },
    )

    assert response.status_code == 201

    session = response.get_json()["session"]

    assert session["goal_id"] == weekly_goal.id


def test_start_invalid_session_type(client, test_user):

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "session_type": "invalid_type",
        },
    )

    assert response.status_code == 400


def test_start_invalid_user(client):

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": 999999,
            "session_type": "study",
        },
    )

    assert response.status_code == 404


def test_start_when_active_session_exists(client, test_user):

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "session_type": "study",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "session_type": "revision",
        },
    )

    assert response.status_code == 400


def test_start_invalid_goal(client, test_user):

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "session_type": "study",
            "goal_id": 999999,
        },
    )

    assert response.status_code == 404


def test_start_goal_from_other_user(
    client,
    db_session,
    test_user,
):

    other = User(
        username="other-user",
        email="other@test.com",
        password_hash=generate_password_hash("123456"),
    )

    db_session.add(other)
    db_session.commit()

    year, week, _ = datetime.now(timezone.utc).isocalendar()

    goal = Goal(
        user_id=other.id,
        year=year,
        week_number=week,
        target_hours=5,
    )

    db_session.add(goal)
    db_session.commit()

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "goal_id": goal.id,
            "session_type": "study",
        },
    )

    assert response.status_code == 400


def test_start_goal_from_other_week(
    client,
    db_session,
    test_user,
):

    year, week, _ = datetime.now(timezone.utc).isocalendar()

    other_week = week + 1 if week < 52 else week - 1

    goal = Goal(
        user_id=test_user.id,
        year=year,
        week_number=other_week,
        target_hours=5,
    )

    db_session.add(goal)
    db_session.commit()

    response = client.post(
        "/api/sessions/start",
        json={
            "user_id": test_user.id,
            "goal_id": goal.id,
            "session_type": "study",
        },
    )

    assert response.status_code == 400



# ======================================================
# PAUSE
# ======================================================

def test_pause_running_session(client, db_session, test_user):
    """Deve pausar uma sessão em execução."""

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="running",
        started_at=datetime.now(timezone.utc),
        duration_hours=Decimal("0"),
        paused_seconds=0,
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/pause",
        json={"session_id": session.id},
    )

    assert response.status_code == 200

    db_session.refresh(session)

    assert session.status == "paused"
    assert session.paused_at is not None


def test_pause_already_paused_session(client, db_session, test_user):
    """Não deve permitir pausar uma sessão já pausada."""

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="paused",
        started_at=datetime.now(timezone.utc),
        paused_at=datetime.now(timezone.utc),
        duration_hours=Decimal("0"),
        paused_seconds=0,
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/pause",
        json={"session_id": session.id},
    )

    assert response.status_code == 400


def test_pause_finished_session(client, db_session, test_user):
    """Não deve permitir pausar sessão finalizada."""

    now = datetime.now(timezone.utc)

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="finished",
        started_at=now,
        finished_at=now,
        duration_hours=Decimal("1"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/pause",
        json={"session_id": session.id},
    )

    assert response.status_code == 400


def test_pause_cancelled_session(client, db_session, test_user):
    """Não deve permitir pausar sessão cancelada."""

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="cancelled",
        started_at=datetime.now(timezone.utc),
        duration_hours=Decimal("0"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/pause",
        json={"session_id": session.id},
    )

    assert response.status_code == 400


def test_pause_nonexistent_session(client):
    """Sessão inexistente deve retornar 404."""

    response = client.post(
        "/api/sessions/pause",
        json={"session_id": 999999},
    )

    assert response.status_code == 404

# ======================================================
# RESUME
# ======================================================

def test_resume_paused_session(client, db_session, test_user):
    """Deve retomar uma sessão pausada."""

    paused_at = datetime.now(timezone.utc)

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="paused",
        started_at=datetime.now(timezone.utc),
        paused_at=paused_at,
        paused_seconds=0,
        duration_hours=Decimal("0"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/resume",
        json={"session_id": session.id},
    )

    assert response.status_code == 200

    db_session.refresh(session)

    assert session.status == "running"
    assert session.paused_at is None
    assert session.paused_seconds >= 0

def test_resume_running_session(client, db_session, test_user):
    """Não deve retomar sessão já em execução."""

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="running",
        started_at=datetime.now(timezone.utc),
        paused_seconds=0,
        duration_hours=Decimal("0"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/resume",
        json={"session_id": session.id},
    )

    assert response.status_code == 400

def test_resume_finished_session(client, db_session, test_user):
    """Não deve retomar sessão finalizada."""

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="finished",
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
        duration_hours=Decimal("1"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/resume",
        json={"session_id": session.id},
    )

    assert response.status_code == 400

def test_resume_cancelled_session(client, db_session, test_user):
    """Não deve retomar sessão cancelada."""

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="cancelled",
        started_at=datetime.now(timezone.utc),
        duration_hours=Decimal("0"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/resume",
        json={"session_id": session.id},
    )

    assert response.status_code == 400

def test_resume_nonexistent_session(client):
    """Não deve retomar sessão inexistente."""

    response = client.post(
        "/api/sessions/resume",
        json={"session_id": 999999},
    )

    assert response.status_code == 404



# ======================================================
# FINISH
# ======================================================

def test_finish_running_session(client, db_session, test_user):
    """Deve finalizar uma sessão em execução."""

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="running",
        started_at=datetime.now(timezone.utc),
        duration_hours=Decimal("0"),
        paused_seconds=0,
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/finish",
        json={"session_id": session.id},
    )

    assert response.status_code == 200

    db_session.refresh(session)

    assert session.status == "finished"
    assert session.finished_at is not None
    assert session.duration_hours >= Decimal("0")


def test_finish_paused_session(client, db_session, test_user):
    """Deve finalizar uma sessão pausada."""

    now = datetime.now(timezone.utc)

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="paused",
        started_at=now,
        paused_at=now,
        paused_seconds=10,
        duration_hours=Decimal("0"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/finish",
        json={"session_id": session.id},
    )

    assert response.status_code == 200

    db_session.refresh(session)

    assert session.status == "finished"
    assert session.paused_at is None
    assert session.finished_at is not None


def test_finish_finished_session(client, db_session, test_user):
    """Não deve finalizar uma sessão já finalizada."""

    now = datetime.now(timezone.utc)

    session = Session(
        user_id=test_user.id,
        session_type="study",
        status="finished",
        started_at=now,
        finished_at=now,
        duration_hours=Decimal("1"),
    )

    db_session.add(session)
    db_session.commit()

    response = client.post(
        "/api/sessions/finish",
        json={"session_id": session.id},
    )

    assert response.status_code == 400


def test_finish_nonexistent_session(client):
    """Não deve finalizar uma sessão inexistente."""

    response = client.post(
        "/api/sessions/finish",
        json={"session_id": 999999},
    )

    assert response.status_code == 404

# ======================================================
# CANCEL
# ======================================================

# (vazio)

# ======================================================
# SET GOAL
# ======================================================

# (vazio)

# ======================================================
# LIST
# ======================================================

# (vazio)