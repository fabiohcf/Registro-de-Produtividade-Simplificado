# tests/test_api.py

import uuid
from app.models.user import User

def test_get_users(client, db_session):
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(username="Test User API", email=unique_email, password="123456")
    db_session.add(user)
    db_session.commit()

    response = client.get("/api/usuarios/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(u["email"] == unique_email for u in data)
