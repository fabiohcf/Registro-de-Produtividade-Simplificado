# app/routes/api_goals.py

from flask import Blueprint, request, jsonify
from app.models.goal import Goal
from app.models.user import User
from app.database import SessionLocal

api_goals_bp = Blueprint("api_goals_bp", __name__, url_prefix="/api/goals")


def validate_goal_data(data):
    """Valida dados da meta."""
    errors = []

    if not data.get("description"):
        errors.append("Descrição é obrigatória")
    elif len(data["description"].strip()) < 5:
        errors.append("Descrição deve ter pelo menos 5 caracteres")

    if not data.get("category"):
        errors.append("Categoria é obrigatória")
    elif len(data["category"].strip()) < 2:
        errors.append("Categoria deve ter pelo menos 2 caracteres")

    if not data.get("user_id"):
        errors.append("ID do usuário é obrigatório")
    elif not isinstance(data["user_id"], int) or data["user_id"] <= 0:
        errors.append("ID do usuário deve ser um número inteiro positivo")

    target_hours = data.get("target_hours", 0)
    if not isinstance(target_hours, (int, float)) or target_hours <= 0:
        errors.append("Horas alvo deve ser um número positivo")

    return errors


@api_goals_bp.route("/", methods=["GET"])
def list_goals():
    session = SessionLocal()
    try:
        goals = session.query(Goal).all()
        return (
            jsonify(
                [
                    {
                        "id": g.id,
                        "description": g.description,
                        "category": g.category,
                        "target_hours": g.target_hours,
                        "user_id": g.user_id,
                        "created_at": (
                            g.created_at.isoformat() if g.created_at else None
                        ),
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
        user = session.get(User, data["user_id"])
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        goal = Goal(
            user_id=data["user_id"],
            description=data["description"].strip(),
            category=data["category"].strip(),
            target_hours=data["target_hours"],
        )
        session.add(goal)
        session.commit()
        return jsonify({"message": "Meta criada com sucesso!", "goal_id": goal.id}), 201
    finally:
        session.close()
