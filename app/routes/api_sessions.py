# app/routes/api_sessions.py

from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.session import Session
from app.models.goal import Goal
from app.models.user import User

bp_sessions = Blueprint("bp_sessions", __name__, url_prefix="/api/sessions")


@bp_sessions.route("/start", methods=["POST"])
def start_session():
    """Inicia uma nova sessão e salva no banco com hora de início."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    user_id = data.get("user_id")
    goal_id = data.get("goal_id")  # opcional
    if not user_id:
        return jsonify({"error": "ID do usuário é obrigatório"}), 400

    if not isinstance(user_id, int) or user_id <= 0:
        return (
            jsonify({"error": "ID do usuário deve ser um número inteiro positivo"}),
            400,
        )

    with SessionLocal() as db:
        # Verificar se o usuário existe
        user = db.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        # Se goal_id foi informado, validar existência
        goal_ref = None
        if goal_id is not None:
            if not isinstance(goal_id, int) or goal_id <= 0:
                return (
                    jsonify(
                        {"error": "ID da meta deve ser um número inteiro positivo"}
                    ),
                    400,
                )
            goal_ref = db.get(Goal, goal_id)
            if not goal_ref:
                return jsonify({"error": "Meta não encontrada"}), 404

        new_session = Session(
            user_id=user_id,
            goal_id=goal_id if goal_ref else None,
            started_at=datetime.now(timezone.utc),
            finished_at=None,
            duration_hours=0,
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return (
            jsonify(
                {
                    "message": "Sessão iniciada com sucesso",
                    "session_id": new_session.id,
                    "goal_id": new_session.goal_id,
                }
            ),
            201,
        )


@bp_sessions.route("/pause", methods=["POST"])
def pause_session():
    """Pausa uma sessão em andamento."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "ID da sessão é obrigatório"}), 400

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404
        if session_obj.finished_at:
            return jsonify({"error": "Sessão já foi finalizada"}), 400

        session_obj.finished_at = datetime.now(timezone.utc)
        session_obj.duration_hours = (
            session_obj.finished_at - session_obj.started_at
        ).total_seconds() / 3600
        db.commit()
        return (
            jsonify(
                {
                    "message": "Sessão pausada",
                    "duration_hours": float(session_obj.duration_hours),
                }
            ),
            200,
        )


@bp_sessions.route("/restart", methods=["POST"])
def restart_session():
    """Reinicia a sessão, zerando os dados anteriores."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "ID da sessão é obrigatório"}), 400

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404

        session_obj.started_at = datetime.now(timezone.utc)
        session_obj.finished_at = None
        session_obj.duration_hours = 0
        db.commit()
        return jsonify({"message": "Sessão reiniciada com sucesso"}), 200


@bp_sessions.route("/finish", methods=["POST"])
def finish_session():
    """Finaliza a sessão e salva o tempo total."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "ID da sessão é obrigatório"}), 400

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404
        if session_obj.finished_at:
            return jsonify({"error": "Sessão já foi finalizada"}), 400

        session_obj.finished_at = datetime.now(timezone.utc)
        session_obj.duration_hours = (
            session_obj.finished_at - session_obj.started_at
        ).total_seconds() / 3600
        db.commit()
        return (
            jsonify(
                {
                    "message": "Sessão finalizada com sucesso",
                    "duration_hours": float(session_obj.duration_hours),
                }
            ),
            200,
        )


@bp_sessions.route("/set_goal", methods=["POST"])
def set_session_goal():
    """Associa uma sessão existente a uma meta existente."""
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id = data.get("session_id")
    goal_id = data.get("goal_id")

    if not session_id or not goal_id:
        return jsonify({"error": "ID da sessão e ID da meta são obrigatórios"}), 400

    if not isinstance(session_id, int) or not isinstance(goal_id, int):
        return jsonify({"error": "IDs devem ser números inteiros"}), 400

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404

        goal_obj = db.get(Goal, goal_id)
        if not goal_obj:
            return jsonify({"error": "Meta não encontrada"}), 404

        # Garante que a meta pertença ao mesmo usuário (opcional, se desejado)
        if goal_obj.user_id != session_obj.user_id:
            return (
                jsonify({"error": "Meta não pertence ao mesmo usuário da sessão"}),
                400,
            )

        session_obj.goal_id = goal_id
        db.commit()
        return jsonify({"message": "Meta associada à sessão com sucesso"}), 200
