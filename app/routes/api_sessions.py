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


bp_sessions = Blueprint("bp_sessions", __name__, url_prefix="/api/sessions")

# Cria diretório de logs se não existir
os.makedirs("logs", exist_ok=True)


def validate_positive_int(value, name):
    """Valida se value é inteiro positivo"""
    if not isinstance(value, int) or value <= 0:
        return jsonify({"error": f"{name} deve ser um número inteiro positivo"}), 400
    return None


@bp_sessions.route("/start", methods=["POST"])
def start_session():
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    user_id = data.get("user_id")
    goal_id = data.get("goal_id")

    # Valida tipo e positivo
    err = validate_positive_int(user_id, "ID do usuário")
    if err:
        return err
    if goal_id is not None:
        err = validate_positive_int(goal_id, "ID da meta")
        if err:
            return err

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
            "session_id": new_session.id,
            "goal_id": new_session.goal_id
        }), 201


@bp_sessions.route("/pause", methods=["POST"])
def pause_session():
    data = request.json
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    session_id = data.get("session_id")
    err = validate_positive_int(session_id, "ID da sessão")
    if err:
        return err

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

    session_id = data.get("session_id")
    err = validate_positive_int(session_id, "ID da sessão")
    if err:
        return err

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

    session_id = data.get("session_id")
    if not session_id or not isinstance(session_id, int) or session_id <= 0:
        return jsonify({"error": "ID da sessão é obrigatório e deve ser um inteiro positivo"}), 400

    with SessionLocal() as db:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Sessão não encontrada"}), 404

        if session_obj.finished_at is not None:
            return jsonify({"error": "Sessão já foi finalizada"}), 400

        if session_obj.started_at is None:
            log_action(session_obj.user_id, session_obj.id, "finish_failed_no_start")
            print(f"DEBUG: session_obj.started_at is None? {session_obj.started_at}") 
            return jsonify({"error": "Sessão não foi iniciada corretamente"}), 400
        else:
            print(f"DEBUG: session_obj.started_at = {session_obj.started_at}")

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

    session_id = data.get("session_id")
    goal_id = data.get("goal_id")

    err1 = validate_positive_int(session_id, "ID da sessão")
    err2 = validate_positive_int(goal_id, "ID da meta")
    if err1:
        return err1
    if err2:
        return err2

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
    user_id = request.args.get("user_id", type=int)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    err = validate_positive_int(user_id, "ID do usuário")
    if err:
        return err

    with SessionLocal() as db:
        query = db.query(Session).filter(Session.user_id == user_id)
        if start_date:
            query = query.filter(Session.started_at >= start_date)
        if end_date:
            query = query.filter(Session.started_at <= end_date)
        sessions = query.all()

        return jsonify([{
            "id": s.id,
            "started_at": s.started_at.isoformat(),
            "finished_at": s.finished_at.isoformat() if s.finished_at else None,
            "duration_hours": float(s.duration_hours) if s.duration_hours else 0,
            "goal_id": s.goal_id
        } for s in sessions]), 200
