from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    path: str
    description: Optional[str] = None
    status: str = Field(default="active")
    tech_stack: Optional[str] = None
    estimated_hours: Optional[int] = None
    repo_url: Optional[str] = None
