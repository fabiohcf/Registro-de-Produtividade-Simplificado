# app/tests/test_users.py

import uuid
from app.models.user import User

def test_create_user(client, db_session):
    unique_email = f"{uuid.uuid4()}@example.com"
    user_data = {"username": "Test User", "email": unique_email, "password": "123456"}

    response = client.post("/api/usuarios/", json=user_data)
    assert response.status_code == 201

    db_user = db_session.query(User).filter_by(email=unique_email).first()
    assert db_user is not None
    assert db_user.username == "Test User"
