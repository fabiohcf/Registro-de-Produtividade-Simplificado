# app/routes/api_sessions.py

from flask import Blueprint, request, jsonify
from decimal import Decimal
from datetime import datetime, timezone
from app.models.session import Session
from app.database import SessionLocal
from app.utils.logging_utils import log_action
from app.models.goal import Goal
from app.models.user import User
import os
import uuid

bp_sessions = Blueprint("bp_sessions", __name__, url_prefix="/api/sessions")

# Cria diretório de logs se não existir
os.makedirs("logs", exist_ok=True)


def validate_uuid(value, name):
    """Valida se value é um UUID válido"""
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError):
        return jsonify({"error": f"{name} inválido"}), 400


# ----------------- ROTAS -----------------

@bp_sessions.route("/start", methods=["POST"])
def start_session():
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    user_id_raw = data.get("user_id")
    goal_id_raw = data.get("goal_id")

    user_id = validate_uuid(user_id_raw, "ID do usuário")
    if isinstance(user_id, tuple):  # erro
        return user_id

    goal_id = None
    if goal_id_raw:
        goal_id = validate_uuid(goal_id_raw, "ID da meta")
        if isinstance(goal_id, tuple):
            return goal_id

    with SessionLocal() as db:
        user = db.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        active = db.query(Session).filter_by(user_id=user_id, finished_at=None).first()
        if active:
            return jsonify({"error": "Usuário já possui sessão ativa"}), 400

        goal_ref = db.get(Goal, goal_id) if goal_id else None
        if goal_id and not goal_ref:
            return jsonify({"error": "Meta não encontrada"}), 404

        new_session = Session(
            user_id=user_id,
            goal_id=goal_id if goal_ref else None,
            started_at=datetime.now(timezone.utc),
            finished_at=None,
            duration_hours=0
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        log_action(user_id, new_session.id, "start")

        return jsonify({
            "message": "Sessão iniciada com sucesso",
            "session_id": str(new_session.id),
            "goal_id": str(new_session.goal_id) if new_session.goal_id else None
        }), 201


@bp_sessions.route("/pause", methods=["POST"])
def pause_session():
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id_raw = data.get("session_id")
    session_id = validate_uuid(session_id_raw, "ID da sessão")
    if isinstance(session_id, tuple):
        return session_id

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404
        if session_obj.finished_at:
            return jsonify({"error": "Sessão já foi finalizada"}), 400
        if not session_obj.started_at:
            return jsonify({"error": "Sessão não foi iniciada corretamente"}), 400

        session_obj.finished_at = datetime.now(timezone.utc)
        session_obj.duration_hours = (session_obj.finished_at - session_obj.started_at).total_seconds() / 3600
        db.commit()

        log_action(session_obj.user_id, session_obj.id, "pause")

        return jsonify({
            "message": "Sessão pausada",
            "duration_hours": float(session_obj.duration_hours)
        }), 200


@bp_sessions.route("/restart", methods=["POST"])
def restart_session():
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id_raw = data.get("session_id")
    session_id = validate_uuid(session_id_raw, "ID da sessão")
    if isinstance(session_id, tuple):
        return session_id

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404

        session_obj.started_at = datetime.now(timezone.utc)
        session_obj.finished_at = None
        session_obj.duration_hours = 0
        db.commit()

        log_action(session_obj.user_id, session_obj.id, "restart")

        return jsonify({"message": "Sessão reiniciada com sucesso"}), 200


@bp_sessions.route("/finish", methods=["POST"])
def finish_session():
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id_raw = data.get("session_id")
    session_id = validate_uuid(session_id_raw, "ID da sessão")
    if isinstance(session_id, tuple):
        return session_id

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404

        if session_obj.finished_at is not None:
            return jsonify({"error": "Sessão já foi finalizada"}), 400
        if session_obj.started_at is None:
            log_action(session_obj.user_id, session_obj.id, "finish_failed_no_start")
            return jsonify({"error": "Sessão não foi iniciada corretamente"}), 400

        session_obj.finished_at = datetime.now(timezone.utc)
        session_obj.duration_hours = Decimal(
            (session_obj.finished_at - session_obj.started_at).total_seconds() / 3600
        )
        db.commit()

        log_action(session_obj.user_id, session_obj.id, "finish")

        return jsonify({
            "message": "Sessão finalizada com sucesso",
            "duration_hours": float(session_obj.duration_hours)
        }), 200


@bp_sessions.route("/set_goal", methods=["POST"])
def set_session_goal():
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id_raw = data.get("session_id")
    goal_id_raw = data.get("goal_id")

    session_id = validate_uuid(session_id_raw, "ID da sessão")
    goal_id = validate_uuid(goal_id_raw, "ID da meta")
    if isinstance(session_id, tuple):
        return session_id
    if isinstance(goal_id, tuple):
        return goal_id

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404

        goal_obj = db.get(Goal, goal_id)
        if not goal_obj:
            return jsonify({"error": "Meta não encontrada"}), 404

        if goal_obj.user_id != session_obj.user_id:
            return jsonify({"error": "Meta não pertence ao mesmo usuário da sessão"}), 400

        session_obj.goal_id = goal_id
        db.commit()

        log_action(session_obj.user_id, session_obj.id, "set_goal")

        return jsonify({"message": "Meta associada à sessão com sucesso"}), 200


@bp_sessions.route("/list", methods=["GET"])
def list_sessions():
    user_id_raw = request.args.get("user_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    user_id = validate_uuid(user_id_raw, "ID do usuário")
    if isinstance(user_id, tuple):
        return user_id

    with SessionLocal() as db:
        query = db.query(Session).filter(Session.user_id == user_id)
        if start_date:
            query = query.filter(Session.started_at >= start_date)
        if end_date:
            query = query.filter(Session.started_at <= end_date)
        sessions = query.all()

        return jsonify([{
            "id": str(s.id),
            "started_at": s.started_at.isoformat(),
            "finished_at": s.finished_at.isoformat() if s.finished_at else None,
            "duration_hours": float(s.duration_hours) if s.duration_hours else 0,
            "goal_id": str(s.goal_id) if s.goal_id else None
        } for s in sessions]), 200


@bp_sessions.route("/frontend_finish", methods=["POST"])
def finish_session_frontend():
    """
    Cria e finaliza sessão diretamente a partir dos dados do frontend.
    Espera JSON:
    {
        "user_id": str (UUID),
        "description": str,
        "type": str,
        "netTime": int,   # em segundos
        "grossTime": int  # em segundos
    }
    """
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    user_id_raw = data.get("user_id")
    description = data.get("description", "")
    activity_type = data.get("type", "")
    net_time = data.get("netTime")
    gross_time = data.get("grossTime")

    user_id = validate_uuid(user_id_raw, "user_id")
    if isinstance(user_id, tuple):
        return user_id

    if not activity_type:
        return jsonify({"error": "type obrigatório"}), 400
    if net_time is None or gross_time is None:
        return jsonify({"error": "netTime e grossTime obrigatórios"}), 400

    with SessionLocal() as db:
        user = db.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        now = datetime.now(timezone.utc)

        new_session = Session(
            user_id=user_id,
            description=description,
            type=activity_type,
            started_at=now,
            finished_at=now,
            duration_hours=Decimal(net_time) / 3600
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        log_action(user_id, new_session.id, "finish_frontend")

        return jsonify({
            "message": "Sessão registrada com sucesso",
            "session_id": str(new_session.id)
        }), 201

def validate_uuid(value, field_name):
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError):
        return jsonify({"error": f"{field_name} inválido"}), 400