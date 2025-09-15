# app/__init__.py

from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(testing: bool = False):
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"  # Troque em produção
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"

    if testing:
        # Desativa segurança extra para facilitar testes
        app.config["JWT_COOKIE_SECURE"] = False
        app.config["JWT_COOKIE_CSRF_PROTECT"] = False
        app.config["JWT_REFRESH_CSRF_HEADER_NAME"] = None
        app.config["JWT_COOKIE_CSRF_PROTECT_REFRESH"] = False
    else:
        # Produção com HTTPS e CSRF ativo
        app.config["JWT_COOKIE_SECURE"] = True
        app.config["JWT_COOKIE_CSRF_PROTECT"] = True
        app.config["JWT_CSRF_CHECK_FORM"] = True

    jwt.init_app(app)

    from app.routes.api_users import api_users_bp
    from app.routes.api_goals import api_goals_bp
    from app.routes.api_auth import auth_bp
    from app.routes.main import main_bp

    app.register_blueprint(api_users_bp, url_prefix="/api/usuarios")
    app.register_blueprint(api_goals_bp, url_prefix="/api/metas")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/")

    return app
