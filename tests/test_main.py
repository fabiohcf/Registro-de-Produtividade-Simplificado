# tests/test_main.py

import pytest

def test_index(client):
    """Testa o endpoint raiz da API"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Bem-vindo à API de Registro de Produtividade"

def test_about(client):
    """Testa o endpoint /about"""
    response = client.get("/about")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "API para gerenciar usuários, metas e sessões de produtividade"
    assert data["version"] == "1.0.0"

def test_health(client):
    """Testa o endpoint de healthcheck"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
