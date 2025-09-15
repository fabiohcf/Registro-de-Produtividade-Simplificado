# tests/test_auth.py

import json
import uuid
import pytest
from werkzeug.security import generate_password_hash
from app.models.user import User

def test_login_endpoint(client, db_session):
    """Testa login bem-sucedido e geração de cookies."""
    # Cria usuário para o teste
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(
        username="TestLogin",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    resp = client.post(
        "/auth/login",
        data=json.dumps({"username": "TestLogin", "password": "123456"}),
        content_type="application/json",
    )

    assert resp.status_code == 200
    cookies = resp.headers.getlist("Set-Cookie")
    assert any("access_token_cookie" in c for c in cookies)
    assert any("refresh_token_cookie" in c for c in cookies)
    data = resp.get_json()
    assert data["msg"] == "Login bem-sucedido"

def test_refresh_endpoint(client, db_session):
    """Testa a geração de novo access token via refresh token."""

    # Cria usuário para o teste
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(
        username="TestRefresh",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    # Login para gerar cookies (client já armazena cookies automaticamente)
    login_resp = client.post(
        "/auth/login",
        data=json.dumps({"username": "TestRefresh", "password": "123456"}),
        content_type="application/json",
    )
    assert login_resp.status_code == 200

    # Faz refresh usando o cookie armazenado pelo client
    refresh_resp = client.post("/auth/refresh")
    print(refresh_resp.data)  # mostra o corpo da resposta
    print(refresh_resp.headers)  # mostra os headers, inclusive cookies
    assert refresh_resp.status_code == 200

    json_data = refresh_resp.get_json()
    assert "access_token" in json_data

    # Verifica se access_token_cookie foi retornado
    refresh_resp_cookies = refresh_resp.headers.getlist("Set-Cookie")
    assert any("access_token_cookie" in c for c in refresh_resp_cookies), \
        "access_token_cookie não encontrado no refresh"

def test_login_com_senha_errada(client, db_session):
    """Deve retornar 401 para senha incorreta"""
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(
        username="WrongPassUser",
        email=unique_email,
        password_hash=generate_password_hash("123456")
    )
    db_session.add(user)
    db_session.commit()

    resp = client.post(
        "/auth/login",
        data=json.dumps({"username": "WrongPassUser", "password": "senha_errada"}),
        content_type="application/json"
    )

    assert resp.status_code == 401
    data = resp.get_json()
    assert data["msg"] == "Credenciais inválidas"

def test_refresh_com_token_invalido(client):
    """Deve retornar 422 ou 401 quando o token de refresh é inválido"""
    resp = client.post("/auth/refresh", headers={
        "Cookie": "refresh_token_cookie=token_invalido"
    })
    assert resp.status_code in (401, 422)

def test_refresh_sem_cookie(client):
    """Deve retornar 422 ou 401 ao tentar refresh sem cookie"""
    resp = client.post("/auth/refresh")
    assert resp.status_code in (401, 422)

def test_login_failure(client, db_session):
    """Testa login com usuário inexistente ou senha incorreta."""
    # Usuário que não existe
    resp = client.post(
        "/auth/login",
        data=json.dumps({"username": "UsuarioInvalido", "password": "senhaqualquer"}),
        content_type="application/json"
    )
    assert resp.status_code == 401
    data = resp.get_json()
    assert data["msg"] == "Credenciais inválidas"

    # Criar usuário válido para testar senha incorreta
    unique_email = f"{uuid.uuid4()}@example.com"
    user = User(
        username="UsuarioValido",
        email=unique_email,
        password_hash=generate_password_hash("senha_correta")
    )
    db_session.add(user)
    db_session.commit()

    # Tenta login com senha errada
    resp2 = client.post(
        "/auth/login",
        data=json.dumps({"username": "UsuarioValido", "password": "senha_errada"}),
        content_type="application/json"
    )
    assert resp2.status_code == 401
    data2 = resp2.get_json()
    assert data2["msg"] == "Credenciais inválidas"
