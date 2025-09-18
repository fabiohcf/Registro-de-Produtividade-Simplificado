# app/routes/api_users.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.database import SessionLocal

api_users_bp = Blueprint("api_users_bp", __name__, url_prefix="/api/users")

@api_users_bp.route("/", methods=["POST"])
def create_user():
    """Cria um novo usuário com hash de senha."""
    data = request.json
    with SessionLocal() as session:
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"])
        )
        session.add(user)
        session.commit()
        return jsonify({"message": "Usuário criado com sucesso!", "user_id": user.id}), 201

@api_users_bp.route("/", methods=["GET"])
def list_users():
    """Lista todos os usuários."""
    with SessionLocal() as session:
        users = session.query(User).all()
        return jsonify([
            {"id": u.id, "username": u.username, "email": u.email}
            for u in users
        ]), 200

@api_users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Busca usuário por ID usando Session.get() profissional."""
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404
        return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200

@api_users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deleta usuário por ID."""
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404
        session.delete(user)
        session.commit()
        return jsonify({"message": "Usuário deletado com sucesso."}), 200

@api_users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Atualiza dados do usuário (username e email)."""
    data = request.json
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso."}), 200
