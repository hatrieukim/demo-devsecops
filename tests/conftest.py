import time

import psycopg
import pytest

from app.db import connect


@pytest.fixture(scope="session")
def db_conn():
    """Connect to Postgres, retrying while the service container starts up."""
    deadline = time.monotonic() + 30
    while True:
        try:
            conn = connect()
            break
        except psycopg.OperationalError:
            if time.monotonic() > deadline:
                raise
            time.sleep(1)
    yield conn
    conn.close()
