# app/tests/test_auth.py

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

def test_login(db_session):
    unique_email = f"{uuid.uuid4()}@example.com"

    # Cria o usuário com senha hash
    user = User(
        username="Auth User",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    # Simula login
    assert check_password_hash(user.password_hash, "123456") is True
    assert check_password_hash(user.password_hash, "wrongpass") is False
