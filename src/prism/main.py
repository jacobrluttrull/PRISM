from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .db import create_db_and_tables, get_session
from .models import Project

app = FastAPI(title="PRISM")

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/")
def index(request: Request, session: Session = Depends(get_session)):
    projects = session.exec(select(Project).order_by(Project.id)).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "projects": projects}
    )


@app.get("/projects/new")
def project_new(request: Request):
    return templates.TemplateResponse("project_new.html", {"request": request})


@app.post("/projects/new")
def project_create(
    request: Request,
    name: str = Form(...),
    path: str = Form(...),
    description: Optional[str] = Form(None),
    status: str = Form("active"),
    tech_stack: Optional[str] = Form(None),
    estimated_hours: Optional[str] = Form(None),
    repo_url: Optional[str] = Form(None),
    session: Session = Depends(get_session),
):
    cleaned_name = name.strip()
    cleaned_path = str(Path(path).expanduser())
    cleaned_description = description.strip() if description else None
    cleaned_status = status.strip().lower()
    cleaned_tech_stack = tech_stack.strip() if tech_stack else None
    cleaned_estimated_hours = None
    cleaned_repo_url = repo_url.strip() if repo_url else None

    if cleaned_description == "":
        cleaned_description = None
    if cleaned_tech_stack == "":
        cleaned_tech_stack = None
    if cleaned_repo_url == "":
        cleaned_repo_url = None

    if not cleaned_name:
        raise HTTPException(status_code=400, detail="Project name is required.")
    if cleaned_status not in {"active", "paused", "archived"}:
        raise HTTPException(status_code=400, detail="Invalid status value.")
    if estimated_hours:
        try:
            cleaned_estimated_hours = int(estimated_hours)
        except ValueError as exc:
            raise HTTPException(
                status_code=400, detail="Estimated hours must be a whole number."
            ) from exc
        if cleaned_estimated_hours < 0:
            raise HTTPException(
                status_code=400, detail="Estimated hours cannot be negative."
            )

    project = Project(
        name=cleaned_name,
        path=cleaned_path,
        description=cleaned_description,
        status=cleaned_status,
        tech_stack=cleaned_tech_stack,
        estimated_hours=cleaned_estimated_hours,
        repo_url=cleaned_repo_url,
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    return RedirectResponse(url=f"/projects/{project.id}", status_code=303)


@app.get("/projects/{project_id}")
def project_detail(
    project_id: int, request: Request, session: Session = Depends(get_session)
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    return templates.TemplateResponse(
        "project_detail.html", {"request": request, "project": project}
    )
