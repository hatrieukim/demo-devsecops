from fastapi.testclient import TestClient

from app.main import app


def test_connect_and_select_one(db_conn):
    assert db_conn.execute("SELECT 1").fetchone() == (1,)


def test_insert_and_query(db_conn):
    db_conn.execute("CREATE TEMP TABLE greetings (id serial PRIMARY KEY, text text)")
    db_conn.execute("INSERT INTO greetings (text) VALUES (%s)", ("hello",))
    row = db_conn.execute("SELECT text FROM greetings WHERE id = 1").fetchone()
    assert row == ("hello",)


def test_db_check_endpoint(db_conn):
    response = TestClient(app).get("/db-check")
    assert response.json() == {"db": True}
