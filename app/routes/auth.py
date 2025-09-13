# app/routes/api_auth.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.models.user import User  # Supondo que User exista
from app.database import engine, Base, sessionmaker

auth_bp = Blueprint("auth", __name__)

# Login: gera access e refresh tokens
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Usuário e senha são obrigatórios"}), 400

    db_session = sessionmaker(bind=engine)()
    user = db_session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    return jsonify({"msg": "Usuário ou senha inválidos"}), 401

# Refresh token: gera novo access token
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access}), 200

# Logout: endpoint inicial, podemos evoluir para blacklist
@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"msg": "Logout realizado (simulado)"}), 200
