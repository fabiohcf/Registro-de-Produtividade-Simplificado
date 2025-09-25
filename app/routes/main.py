# app/routes/main.py

from flask import Blueprint, jsonify, request
from app.utils.logging_utils import log_general

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    """Endpoint raiz da API."""
    log_general("Acesso ao endpoint /")
    return jsonify({"message": "Bem-vindo à API de Registro de Produtividade"}), 200

@main_bp.route("/about", methods=["GET"])
def about():
    """Informações sobre a API."""
    log_general("Acesso ao endpoint /about")
    return jsonify({
        "message": "API para gerenciar usuários, metas e sessões de produtividade",
        "version": "1.0.0"
    }), 200

@main_bp.route("/health", methods=["GET"])
def health():
    """Endpoint de healthcheck para monitoramento."""
    log_general("Healthcheck executado")
    return jsonify({"status": "ok"}), 200