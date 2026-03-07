# config/testing.py

import os

class TestingConfig:
    TESTING = True

    # banco isolado para testes
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_produtividade.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # desativa JWT real se necessário
    JWT_SECRET_KEY = "test-secret-key"

    # logs menores
    LOG_LEVEL = "WARNING"