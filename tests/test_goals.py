# app/tests/test_goals.py

import uuid
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.goal import Goal
import pytest


def test_create_goal(client, db_session):
    # Cria usuário com UUID
    user = User(
        username=f"User Goal {uuid.uuid4()}",
        email=f"{uuid.uuid4()}@example.com",
        password_hash=generate_password_hash("123456"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    goal_data = {
        "user_id": str(user.id),  # UUID como string
        "description": "Aprender Python",
        "category": "Study",
        "target_hours": 10,
    }

    response = client.post("/api/goals/", json=goal_data)
    assert response.status_code == 201

    db_goal = db_session.query(Goal).filter_by(description="Aprender Python").first()
    assert db_goal is not None
    assert str(db_goal.user_id) == str(user.id)


def test_create_goal_invalid_data(client):
    # UUID de usuário inválido para teste
    invalid_uuid = str(uuid.uuid4())

    payloads = [
        {"description": "", "category": "Study", "target_hours": 10, "user_id": invalid_uuid},
        {"description": "Aprender Flask", "category": "Study", "target_hours": -5, "user_id": invalid_uuid},
        {"description": "Aprender Flask", "category": "Study", "target_hours": 10},  # sem user_id
    ]

    for payload in payloads:
        response = client.post("/api/goals/", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "inválido" in data["error"].lower()
