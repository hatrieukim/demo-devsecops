import os

import psycopg

DEFAULT_URL = "postgresql://app:app@localhost:5432/app"


def database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_URL)


def connect() -> psycopg.Connection:
    return psycopg.connect(database_url(), connect_timeout=5)


def fetch_one(sql: str, params: tuple = ()) -> tuple:
    with connect() as conn:
        return conn.execute(sql, params).fetchone()
