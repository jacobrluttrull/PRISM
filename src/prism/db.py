from __future__ import annotations

import os
from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine


def get_database_url() -> str:
    db_path = Path.cwd() / "prism.db"
    if os.name == "nt":
        return f"sqlite:///{db_path.as_posix()}"
    return f"sqlite:///{db_path}"


engine = create_engine(get_database_url(), connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
