# app/routes/api_auth.py

from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint("auth", __name__)

# Rota de login para gerar tokens
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username != "TestRefresh" or password != "123456":
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    resp = make_response(jsonify({"msg": "Login bem-sucedido"}))
    resp.set_cookie("access_token_cookie", access_token, httponly=True)
    resp.set_cookie("refresh_token_cookie", refresh_token, httponly=True)
    return resp, 200

# Rota para renovar access token usando refresh token
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token}), 200
