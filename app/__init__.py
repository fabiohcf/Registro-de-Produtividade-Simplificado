# app/__init__.py

from flask import Flask
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

jwt = JWTManager()


def create_app(testing: bool = False):
    # Carrega variáveis de ambiente de um arquivo .env, se existir
    load_dotenv()
    app = Flask(__name__)

    # Configurações do JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"

    if testing:
        # Facilita testes desativando segurança extra
        app.config["JWT_COOKIE_SECURE"] = False
        app.config["JWT_COOKIE_CSRF_PROTECT"] = False
        app.config["JWT_REFRESH_CSRF_HEADER_NAME"] = None
        app.config["JWT_COOKIE_CSRF_PROTECT_REFRESH"] = False
    else:
        # Produção: HTTPS e CSRF ativo
        app.config["JWT_COOKIE_SECURE"] = True
        app.config["JWT_COOKIE_CSRF_PROTECT"] = True
        app.config["JWT_CSRF_CHECK_FORM"] = True

    # Inicializa JWT
    jwt.init_app(app)

    # Importa blueprints
    from app.routes.api_users import api_users_bp
    from app.routes.api_goals import api_goals_bp
    from app.routes.api_auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.api_sessions import bp_sessions

    # Registra blueprints
    app.register_blueprint(api_users_bp)
    app.register_blueprint(api_goals_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(bp_sessions)

    return app
