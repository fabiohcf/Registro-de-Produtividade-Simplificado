# app/routes/api_goals.py

from flask import Blueprint, request, jsonify
from app.models.goal import Goal
from app.database import SessionLocal

# Blueprint em inglês
api_goals_bp = Blueprint("api_goals_bp", __name__, url_prefix="/api/goals")

@api_goals_bp.route("/", methods=["GET"])
def list_goals():
    session = SessionLocal()
    try:
        goals = session.query(Goal).all()
        # Dados técnicos da API em inglês
        return jsonify([{
            "id": g.id,
            "description": g.description,
            "category": g.category,
            "target_hours": g.target_hours,
            "user_id": g.user_id
        } for g in goals]), 200
    finally:
        session.close()

@api_goals_bp.route("/", methods=["POST"])
def create_goal():
    data = request.json

    # Validação básica
    description = data.get("description", "").strip()
    category = data.get("category", "").strip()
    target_hours = data.get("target_hours", 0)
    user_id = data.get("user_id")

    if not description or target_hours < 0 or not user_id:
        return jsonify({"error": "Dados da meta inválidos"}), 400

    session = SessionLocal()
    try:
        goal = Goal(
            user_id=user_id,
            description=description,
            category=category,
            target_hours=target_hours
        )
        session.add(goal)
        session.commit()
        # Mensagem ao usuário em português
        return jsonify({"message": "Meta criada com sucesso!"}), 201
    finally:
        session.close()
