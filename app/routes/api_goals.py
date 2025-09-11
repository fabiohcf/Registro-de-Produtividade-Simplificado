# app/routes/api_goals.py

from flask import Blueprint, request, jsonify
from app.models.goal import Goal
from app.database import SessionLocal

api_goals_bp = Blueprint("api_goals", __name__)

@api_goals_bp.route("/", methods=["GET"])
def list_goals():
    session = SessionLocal()
    try:
        goals = session.query(Goal).all()
        return jsonify([{
            "id": g.id,
            "description": g.description,
            "category": g.category,  # corrigido de type -> category
            "target_hours": g.target_hours,
            "user_id": g.user_id
        } for g in goals]), 200
    finally:
        session.close()

@api_goals_bp.route("/", methods=["POST"])
def create_goal():
    data = request.json
    session = SessionLocal()
    try:
        goal = Goal(
            user_id=data["user_id"],
            description=data["description"],
            category=data.get("category", ""),  # corrigido de type -> category
            target_hours=data.get("target_hours", 0)
        )
        session.add(goal)
        session.commit()
        return jsonify({"message": "Meta criada com sucesso!"}), 201
    finally:
        session.close()
