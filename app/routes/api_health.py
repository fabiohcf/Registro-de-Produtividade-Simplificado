# app/routes/api_health.py
from flask import Blueprint, jsonify

api_health_bp = Blueprint("api_health", __name__, url_prefix="/api/health")

@api_health_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})
