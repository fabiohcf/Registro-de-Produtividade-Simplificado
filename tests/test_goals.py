# app/tests/test_goals.py

import uuid
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.goal import Goal
import pytest

def test_create_goal(client, db_session):
    unique_email = f"{uuid.uuid4()}@example.com"

    # Cria o usuário com hash da senha
    user = User(
        username="User Goal",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    goal_data = {
        "user_id": user.id,
        "description": "Aprender Python",
        "category": "Study",
        "target_hours": 10
    }
    response = client.post("/api/goals/", json=goal_data)
    assert response.status_code == 201

    db_goal = db_session.query(Goal).filter_by(description="Aprender Python").first()
    assert db_goal is not None
    assert db_goal.user_id == user.id

def test_create_goal_invalid_data(client):
    # Dados inválidos: descrição vazia, target_hours negativo, user_id ausente
    payloads = [
        {"description": "", "category": "Study", "target_hours": 10, "user_id": 1},
        {"description": "Aprender Flask", "category": "Study", "target_hours": -5, "user_id": 1},
        {"description": "Aprender Flask", "category": "Study", "target_hours": 10}  # sem user_id
    ]

    for payload in payloads:
        response = client.post("/api/goals/", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "inválido" in data["error"].lower()
