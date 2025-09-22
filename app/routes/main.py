# app/routes/main.py

from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__, url_prefix="/")

@main_bp.route("/", methods=["GET"])
def index():
    return "Página inicial", 200

@main_bp.route("/about", methods=["GET"])
def about():
    return "Página sobre o sistema.", 200
