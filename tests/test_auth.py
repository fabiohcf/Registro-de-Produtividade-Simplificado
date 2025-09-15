# tests/test_auth.py

import json
from app.models import User
from werkzeug.security import generate_password_hash

def test_login_endpoint(client):
    resp = client.post(
        "/auth/login",
        data=json.dumps({"username": "TestRefresh", "password": "123456"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert "Set-Cookie" in resp.headers

def test_refresh_endpoint(client):
    # Login para gerar cookies
    login_resp = client.post(
        "/auth/login",
        data=json.dumps({"username": "TestRefresh", "password": "123456"}),
        content_type="application/json",
    )
    assert login_resp.status_code == 200

    # Extrai refresh_token_cookie
    cookies = login_resp.headers.getlist("Set-Cookie")
    refresh_cookie = None
    for c in cookies:
        if "refresh_token_cookie" in c:
            refresh_cookie = c.split(";")[0].split("=", 1)[1]
            break
    assert refresh_cookie, "Refresh token não encontrado nos cookies"

    # Usa o refresh_token para pedir novo access token
    refresh_resp = client.post(
        "/auth/refresh",
        headers={"Cookie": f"refresh_token_cookie={refresh_cookie}"}
    )
    print("Resposta do refresh:", refresh_resp.json)
    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.json


    def test_refresh_com_token_invalido(client):
        """Deve retornar 422 quando o token de refresh é inválido"""
        resp = client.post("/auth/refresh", headers={
            "Cookie": "refresh_token_cookie=token_invalido"
        })
        assert resp.status_code in (401, 422)


    def test_login_com_senha_errada(client, db_session):
        """Deve retornar 401 para senha incorreta"""
        user = User(
            username="WrongPassUser",
            email="wrongpass@example.com",
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


    def test_refresh_sem_cookie(client):
        """Deve retornar 422 ao tentar refresh sem cookie"""
        resp = client.post("/auth/refresh")
        assert resp.status_code in (401, 422)
