from fastapi import FastAPI

from app.db import fetch_one

app = FastAPI(title="hello API")


@app.get("/hello")
def hello() -> dict:
    return {"message": "hello"}


@app.get("/db-check")
def db_check() -> dict:
    return {"db": fetch_one("SELECT 1")[0] == 1}
