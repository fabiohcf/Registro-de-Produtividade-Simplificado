# app/routes/auth.py

from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "Login simulado"}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout realizado com sucesso"}), 200
