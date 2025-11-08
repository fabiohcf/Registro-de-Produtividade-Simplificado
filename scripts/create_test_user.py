# scripts/create_test_user.py

import uuid
from werkzeug.security import generate_password_hash
from app.database import SessionLocal
from app.models.user import User

# UUID fixo do usuário de teste (o mesmo que você vai colocar no localStorage do frontend)
TEST_USER_UUID = "550e8400-e29b-41d4-a716-446655440000"

def create_test_user():
    session = SessionLocal()
    try:
        # Verifica se o usuário já existe
        existing_user = session.query(User).filter_by(id=TEST_USER_UUID).first()
        if existing_user:
            print(f"Usuário já existe: {existing_user.username} ({TEST_USER_UUID})")
            return

        # Cria novo usuário de teste
        user = User(
            id=TEST_USER_UUID,
            username="Frontend Test User",
            email=f"frontend_test_{uuid.uuid4()}@example.com",
            password_hash=generate_password_hash("123456")
        )
        session.add(user)
        session.commit()
        print(f"Usuário criado com sucesso! UUID: {TEST_USER_UUID}")
    finally:
        session.close()


if __name__ == "__main__":
    create_test_user()
