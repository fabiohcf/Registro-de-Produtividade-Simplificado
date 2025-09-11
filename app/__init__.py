# app/__init__.py

import os
from flask import Flask
from app.database import Base, engine
from app.routes.api_users import api_users_bp
from app.routes.api_goals import api_goals_bp
from app.routes.auth import auth_bp
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # Registra blueprints com prefixos
    app.register_blueprint(api_users_bp, url_prefix="/api/usuarios")
    app.register_blueprint(api_goals_bp, url_prefix="/api/metas")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)  # rotas de página (/, /sobre etc.)

    # Cria tabelas na inicialização do app
    with app.app_context():
        Base.metadata.create_all(bind=engine)

    return app
