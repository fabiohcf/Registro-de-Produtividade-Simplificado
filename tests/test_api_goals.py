# tests/test_api_goals.py

import uuid
import pytest
from app.models.goal import Goal
from app.models.user import User
from app.database import SessionLocal


@pytest.fixture
def sample_user():
    """Cria um usuário temporário para os testes."""
    session = SessionLocal()
    user = User(username="testuser", email="test@example.com", password_hash="1234")
    session.add(user)
    session.commit()
    yield user
    session.delete(user)
    session.commit()
    session.close()


def test_create_goal(client, sample_user):
    """Testa criação de uma meta válida."""
    response = client.post(
        "/api/goals/",
        json={
            "user_id": str(sample_user.id),
            "description": "Estudar Flask avançado",
            "category": "study",
            "target_hours": 10,
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "goal_id" in data


def test_create_goal_invalid_data(client):
    """Testa criação de meta com dados inválidos."""
    response = client.post(
        "/api/goals/",
        json={"description": "Oi", "category": "", "target_hours": -5},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_list_goals(client, sample_user):
    """Testa listagem de metas."""
    session = SessionLocal()
    goal = Goal(
        user_id=sample_user.id,
        description="Meta de teste",
        category="work",
        target_hours=8,
    )
    session.add(goal)
    session.commit()

    response = client.get("/api/goals/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(g["description"] == "Meta de teste" for g in data)

    session.delete(goal)
    session.commit()
    session.close()


def test_update_goal(client, sample_user):
    """Testa atualização de uma meta."""
    session = SessionLocal()
    goal = Goal(
        user_id=sample_user.id,
        description="Meta inicial",
        category="study",
        target_hours=5,
    )
    session.add(goal)
    session.commit()

    response = client.put(
        f"/api/goals/{goal.id}",
        json={"description": "Meta atualizada", "target_hours": 12},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "atualizada" in data["message"]

    session.delete(goal)
    session.commit()
    session.close()


def test_delete_goal(client, sample_user):
    """Testa exclusão de meta."""
    session = SessionLocal()
    goal = Goal(
        user_id=sample_user.id,
        description="Meta temporária",
        category="study",
        target_hours=3,
    )
    session.add(goal)
    session.commit()

    response = client.delete(f"/api/goals/{goal.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert "excluída" in data["message"]

    # Abre nova sessão para verificar o estado real no banco
    session.close()
    new_session = SessionLocal()
    deleted = new_session.get(Goal, goal.id)
    assert deleted is None
    new_session.close()