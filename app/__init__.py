# app/__init__.py

from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configurações do JWT
    app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"  # Troque em produção
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"
    app.config["JWT_COOKIE_SECURE"] = False  # True em produção com HTTPS
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Desativado para testes

    jwt.init_app(app)

    # Importa e registra blueprints
    from app.routes.api_users import api_users_bp
    from app.routes.api_goals import api_goals_bp
    from app.routes.api_auth import auth_bp
    from app.routes.main import main_bp

    app.register_blueprint(api_users_bp, url_prefix="/api/usuarios")
    app.register_blueprint(api_goals_bp, url_prefix="/api/metas")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/")

    return app
