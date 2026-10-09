from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_returns_message():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}


def test_unknown_route_returns_404():
    assert client.get("/nope").status_code == 404
