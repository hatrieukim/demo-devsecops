import os

from fastapi import FastAPI

from app.db import fetch_one

app = FastAPI(title="hello API")


@app.get("/hello")
def hello() -> dict:
    return {"message": "hello"}


@app.get("/db-check")
def db_check() -> dict:
    return {"db": fetch_one("SELECT 1")[0] == 1}


@app.get("/version")
def version() -> dict:
    """Which commit is running and in which environment. Set by the deploy job."""
    return {
        "version": os.environ.get("APP_VERSION", "dev"),
        "environment": os.environ.get("APP_ENV", "local"),
    }
