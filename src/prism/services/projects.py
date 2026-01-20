from __future__ import annotations

from pathlib import Path
from typing import Optional

from sqlmodel import Session, select

from ..models import Project

ALLOWED_STATUSES = {"active", "paused", "archived"}


def normalize_project_inputs(
    name: str,
    path: str,
    description: Optional[str],
    status: str,
    tech_stack: Optional[str],
    estimated_hours: Optional[str],
    repo_url: Optional[str],
) -> dict:
    cleaned_name = name.strip()
    cleaned_path = str(Path(path).expanduser())
    cleaned_description = _clean_optional(description)
    cleaned_status = status.strip().lower()
    cleaned_tech_stack = _clean_optional(tech_stack)
    cleaned_repo_url = _clean_optional(repo_url)
    cleaned_estimated_hours = None

    if not cleaned_name:
        raise ValueError("Project name is required.")
    if cleaned_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid status value.")
    if estimated_hours:
        try:
            cleaned_estimated_hours = int(estimated_hours)
        except ValueError as exc:
            raise ValueError("Estimated hours must be a whole number.") from exc
        if cleaned_estimated_hours < 0:
            raise ValueError("Estimated hours cannot be negative.")

    return {
        "name": cleaned_name,
        "path": cleaned_path,
        "description": cleaned_description,
        "status": cleaned_status,
        "tech_stack": cleaned_tech_stack,
        "estimated_hours": cleaned_estimated_hours,
        "repo_url": cleaned_repo_url,
    }


def list_projects(session: Session) -> list[Project]:
    return session.exec(select(Project).order_by(Project.id)).all()


def get_project(session: Session, project_id: int) -> Optional[Project]:
    return session.get(Project, project_id)


def create_project(session: Session, project_data: dict) -> Project:
    project = Project(**project_data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(session: Session, project: Project, project_data: dict) -> Project:
    for key, value in project_data.items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()


def _clean_optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None
