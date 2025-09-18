# app/routes/api_sessions.py

from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.session import Session


bp_sessions = Blueprint("bp_sessions", __name__, url_prefix="/api/sessions")

@bp_sessions.route("/start", methods=["POST"])
def start_session():
    """Inicia uma nova sessão e salva no banco com hora de início."""
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required."}), 400

    db = SessionLocal()
    try:
        new_session = Session(
            user_id=user_id,
            started_at=datetime.now(timezone.utc),
            finished_at=None,
            duration_hours=0
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return jsonify({"message": "Session started successfully.", "session_id": new_session.id}), 201
    finally:
        db.close()

@bp_sessions.route("/pause", methods=["POST"])
def pause_session():
    """Pausa uma sessão em andamento."""
    session_id = request.json.get("session_id")
    db = SessionLocal()
    try:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Session not found."}), 404
        if session_obj.finished_at:
            return jsonify({"error": "Session already finished."}), 400

        session_obj.finished_at = datetime.now(timezone.utc)
        session_obj.duration_hours = (session_obj.finished_at - session_obj.started_at).total_seconds() / 3600
        db.commit()
        return jsonify({"message": "Session paused.", "duration_hours": session_obj.duration_hours}), 200
    finally:
        db.close()

@bp_sessions.route("/restart", methods=["POST"])
def restart_session():
    """Reinicia a sessão, zerando os dados anteriores."""
    session_id = request.json.get("session_id")
    db = SessionLocal()
    try:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Session not found."}), 404

        session_obj.started_at = datetime.now(timezone.utc)
        session_obj.finished_at = None
        session_obj.duration_hours = 0
        db.commit()
        return jsonify({"message": "Session restarted successfully."}), 200
    finally:
        db.close()

@bp_sessions.route("/finish", methods=["POST"])
def finish_session():
    """Finaliza a sessão e salva o tempo total."""
    session_id = request.json.get("session_id")
    db = SessionLocal()
    try:
        session_obj = db.get(Session, session_id)
        if not session_obj:
            return jsonify({"error": "Session not found."}), 404
        if session_obj.finished_at:
            return jsonify({"error": "Session already finished."}), 400

        session_obj.finished_at = datetime.now(timezone.utc)
        session_obj.duration_hours = (session_obj.finished_at - session_obj.started_at).total_seconds() / 3600
        db.commit()
        return jsonify({
            "message": "Session finished successfully.",
            "duration_hours": session_obj.duration_hours
        }), 200
    finally:
        db.close()
