from datetime import datetime, timezone
import uuid
import pytest
from werkzeug.security import generate_password_hash

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

# (vazio por enquanto)

# ======================================================
# RESUME
# ======================================================

# (vazio)

# ======================================================
# FINISH
# ======================================================

# (vazio)

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