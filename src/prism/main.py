from __future__ import annotations

from fastapi import FastAPI

from .db import create_db_and_tables
from .routes.projects import router as projects_router

app = FastAPI(title="PRISM")
app.include_router(projects_router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()
