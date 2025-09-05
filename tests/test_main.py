# app/tests/test_main.py

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Página inicial" in response.get_data(as_text=True)

def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert "Página sobre o sistema." in response.get_data(as_text=True)
