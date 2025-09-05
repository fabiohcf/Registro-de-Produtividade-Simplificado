# app/routes/__init__.py

from flask import Flask
from app.routes.api_users import api_users_bp
from app.routes.api_goals import api_goals_bp
from app.routes.auth import auth_bp
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)

    # Registrar blueprints com prefixos coerentes
    app.register_blueprint(api_users_bp, url_prefix="/api/usuarios")  # Rotas de usuários
    app.register_blueprint(api_goals_bp, url_prefix="/api/metas")     # Rotas de metas
    app.register_blueprint(auth_bp, url_prefix="/auth")               # Rotas de autenticação
    app.register_blueprint(main_bp, url_prefix="/")                   # Rotas principais

    return app
