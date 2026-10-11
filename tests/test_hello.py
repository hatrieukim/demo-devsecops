from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_returns_message():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}


def test_ping_returns_pong():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_unknown_route_returns_404():
    assert client.get("/nope").status_code == 404


def test_version_defaults_to_dev():
    assert client.get("/version").json() == {"version": "dev", "environment": "local"}


def test_version_reads_environment(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "abc1234")
    monkeypatch.setenv("APP_ENV", "staging")
    assert client.get("/version").json() == {"version": "abc1234", "environment": "staging"}
