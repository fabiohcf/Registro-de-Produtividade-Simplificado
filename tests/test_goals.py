# app/tests/test_goals.py

import uuid
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.models.goal import Goal

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
        "category": "Study",  # Alterado de type -> category
        "target_hours": 10
    }
    response = client.post("/api/metas/", json=goal_data)
    assert response.status_code == 201

    db_goal = db_session.query(Goal).filter_by(description="Aprender Python").first()
    assert db_goal is not None
    assert db_goal.user_id == user.id
