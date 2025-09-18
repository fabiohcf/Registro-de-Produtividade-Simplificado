# app/routes/api_users.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.database import SessionLocal

# Blueprint em inglês
api_users_bp = Blueprint("api_users_bp", __name__)

@api_users_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    session = SessionLocal()
    try:
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"])  # ✅ usar password_hash
        )
        session.add(user)
        session.commit()
        # Mensagem ao usuário em português
        return jsonify({"message": "Usuário criado com sucesso!"}), 201
    finally:
        session.close()

@api_users_bp.route("/", methods=["GET"])
def list_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        # Retorno de dados técnicos da API
        return jsonify([
            {"id": u.id, "username": u.username, "email": u.email}
            for u in users
        ]), 200
    finally:
        session.close()
