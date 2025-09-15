# tests/test_auth.py

import json

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
