# app/routes/api_goals.py

from flask import Blueprint, request, jsonify
from app.models.goal import Goal
from app.models.user import User
from app.database import SessionLocal
import uuid

api_goals_bp = Blueprint("api_goals_bp", __name__, url_prefix="/api/goals")


def validate_goal_data(data):
    """Valida dados da meta (goal)."""
    errors = []

    # Descrição
    if not data.get("description"):
        errors.append("Descrição é obrigatória")
    elif len(data["description"].strip()) < 5:
        errors.append("Descrição deve ter pelo menos 5 caracteres")

    # Categoria
    if not data.get("category"):
        errors.append("Categoria é obrigatória")
    elif len(data["category"].strip()) < 2:
        errors.append("Categoria deve ter pelo menos 2 caracteres")

    # ID do usuário (UUID)
    user_id = data.get("user_id")
    if not user_id:
        errors.append("ID do usuário é obrigatório")
    else:
        try:
            uuid.UUID(str(user_id))
        except (ValueError, TypeError):
            errors.append("ID do usuário deve ser um UUID válido")

    # Horas alvo
    target_hours = data.get("target_hours", 0)
    if not isinstance(target_hours, (int, float)) or target_hours <= 0:
        errors.append("Horas alvo deve ser um número positivo")

    return errors


@api_goals_bp.route("/", methods=["GET"])
def list_goals():
    """Lista todas as metas registradas."""
    session = SessionLocal()
    try:
        goals = session.query(Goal).all()
        return (
            jsonify(
                [
                    {
                        "id": str(g.id),
                        "description": g.description,
                        "category": g.category,
                        "target_hours": g.target_hours,
                        "user_id": str(g.user_id),
                        "created_at": g.created_at.isoformat() if g.created_at else None,
                    }
                    for g in goals
                ]
            ),
            200,
        )
    finally:
        session.close()


@api_goals_bp.route("/", methods=["POST"])
def create_goal():
    """Cria uma nova meta (goal)."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    # Validações
    errors = validate_goal_data(data)
    if errors:
        return jsonify({"error": "Dados inválidos", "details": errors}), 400

    session = SessionLocal()
    try:
        # Verificar se o usuário existe
        user = session.get(User, uuid.UUID(data["user_id"]))
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        # Criar meta
        goal = Goal(
            user_id=uuid.UUID(data["user_id"]),
            description=data["description"].strip(),
            category=data["category"].strip(),
            target_hours=data["target_hours"],
        )
        session.add(goal)
        session.commit()

        return jsonify(
            {
                "message": "Meta criada com sucesso!",
                "goal_id": str(goal.id),
                "user_id": str(goal.user_id),
            }
        ), 201
    finally:
        session.close()

@api_goals_bp.route("/<uuid:goal_id>", methods=["GET"])
def get_goal(goal_id):
    """Retorna uma meta específica pelo ID."""
    session = SessionLocal()
    try:
        goal = session.get(Goal, goal_id)
        if not goal:
            return jsonify({"error": "Meta não encontrada"}), 404

        return jsonify(
            {
                "id": goal.id,
                "description": goal.description,
                "category": goal.category,
                "target_hours": goal.target_hours,
                "user_id": goal.user_id,
                "created_at": goal.created_at.isoformat() if goal.created_at else None,
            }
        ), 200
    finally:
        session.close()


@api_goals_bp.route("/<uuid:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    """Atualiza uma meta existente."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session = SessionLocal()
    try:
        goal = session.get(Goal, goal_id)
        if not goal:
            return jsonify({"error": "Meta não encontrada"}), 404

        # Atualiza apenas os campos enviados
        if "description" in data:
            if len(data["description"].strip()) < 5:
                return jsonify({"error": "Descrição deve ter pelo menos 5 caracteres"}), 400
            goal.description = data["description"].strip()

        if "category" in data:
            if len(data["category"].strip()) < 2:
                return jsonify({"error": "Categoria deve ter pelo menos 2 caracteres"}), 400
            goal.category = data["category"].strip()

        if "target_hours" in data:
            target = data["target_hours"]
            if not isinstance(target, (int, float)) or target <= 0:
                return jsonify({"error": "Horas alvo deve ser um número positivo"}), 400
            goal.target_hours = target

        session.commit()
        return jsonify({"message": "Meta atualizada com sucesso"}), 200
    finally:
        session.close()


@api_goals_bp.route("/<uuid:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    """Exclui uma meta pelo ID."""
    session = SessionLocal()
    try:
        goal = session.get(Goal, goal_id)
        if not goal:
            return jsonify({"error": "Meta não encontrada"}), 404

        session.delete(goal)
        session.commit()
        return jsonify({"message": "Meta excluída com sucesso"}), 200
    finally:
        session.close()