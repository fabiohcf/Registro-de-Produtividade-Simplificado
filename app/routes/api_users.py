# app/routes/api_users.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
import re
from app.models.user import User
from app.database import SessionLocal

api_users_bp = Blueprint("api_users_bp", __name__, url_prefix="/api/users")


def validate_email(email):
    """Valida formato do email."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_user_data(data, is_update=False):
    """Valida dados do usuário."""
    errors = []

    if not is_update:
        if not data.get("username"):
            errors.append("Username é obrigatório")
        elif len(data["username"]) < 3:
            errors.append("Username deve ter pelo menos 3 caracteres")

        if not data.get("email"):
            errors.append("Email é obrigatório")
        elif not validate_email(data["email"]):
            errors.append("Email deve ter formato válido")

        if not data.get("password"):
            errors.append("Senha é obrigatória")
        elif len(data["password"]) < 6:
            errors.append("Senha deve ter pelo menos 6 caracteres")
    else:
        # Para updates, validar apenas os campos fornecidos
        if "username" in data and len(data["username"]) < 3:
            errors.append("Username deve ter pelo menos 3 caracteres")

        if "email" in data:
            if not validate_email(data["email"]):
                errors.append("Email deve ter formato válido")

    return errors


@api_users_bp.route("/", methods=["POST"])
def create_user():
    """Cria um novo usuário com hash de senha."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    # Validações
    errors = validate_user_data(data)
    if errors:
        return jsonify({"error": "Dados inválidos", "details": errors}), 400

    with SessionLocal() as session:
        try:
            user = User(
                username=data["username"],
                email=data["email"],
                password_hash=generate_password_hash(data["password"]),
            )
            session.add(user)
            session.commit()
            return (
                jsonify({"message": "Usuário criado com sucesso!", "user_id": user.id}),
                201,
            )
        except IntegrityError as e:
            session.rollback()
            if "email" in str(e):
                return jsonify({"error": "Email já está em uso"}), 400
            return jsonify({"error": "Erro ao criar usuário"}), 400


@api_users_bp.route("/", methods=["GET"])
def list_users():
    """Lista todos os usuários."""
    with SessionLocal() as session:
        users = session.query(User).all()
        return (
            jsonify(
                [{"id": u.id, "username": u.username, "email": u.email} for u in users]
            ),
            200,
        )


@api_users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Busca usuário por ID usando Session.get() profissional."""
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return (
            jsonify({"id": user.id, "username": user.username, "email": user.email}),
            200,
        )


@api_users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deleta usuário por ID."""
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        session.delete(user)
        session.commit()
        return jsonify({"message": "Usuário deletado com sucesso"}), 200


@api_users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Atualiza dados do usuário (username e email)."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    # Validações
    errors = validate_user_data(data, is_update=True)
    if errors:
        return jsonify({"error": "Dados inválidos", "details": errors}), 400

    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        try:
            # Atualiza apenas os campos fornecidos
            if "username" in data:
                user.username = data["username"]
            if "email" in data:
                user.email = data["email"]

            session.commit()
            return jsonify({"message": "Usuário atualizado com sucesso"}), 200
        except IntegrityError as e:
            session.rollback()
            if "email" in str(e):
                return jsonify({"error": "Email já está em uso por outro usuário"}), 400
            return jsonify({"error": "Erro ao atualizar usuário"}), 400
