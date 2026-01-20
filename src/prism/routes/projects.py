from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from ..db import get_session
from ..services.projects import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    normalize_project_inputs,
    update_project,
)

router = APIRouter()

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/")
def index(request: Request, session: Session = Depends(get_session)):
    projects = list_projects(session)
    return templates.TemplateResponse(
        "index.html", {"request": request, "projects": projects}
    )


@router.get("/projects/new")
def project_new(request: Request):
    return templates.TemplateResponse("project_new.html", {"request": request})


@router.post("/projects/new")
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
    try:
        project_data = normalize_project_inputs(
            name=name,
            path=path,
            description=description,
            status=status,
            tech_stack=tech_stack,
            estimated_hours=estimated_hours,
            repo_url=repo_url,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    project = create_project(session, project_data)
    return RedirectResponse(url=f"/projects/{project.id}", status_code=303)


@router.get("/projects/{project_id}")
def project_detail(
    project_id: int, request: Request, session: Session = Depends(get_session)
):
    project = get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    return templates.TemplateResponse(
        "project_detail.html", {"request": request, "project": project}
    )


@router.get("/projects/{project_id}/edit")
def project_edit(
    project_id: int, request: Request, session: Session = Depends(get_session)
):
    project = get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    return templates.TemplateResponse(
        "project_edit.html", {"request": request, "project": project}
    )


@router.post("/projects/{project_id}/edit")
def project_update(
    project_id: int,
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
    project = get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    try:
        project_data = normalize_project_inputs(
            name=name,
            path=path,
            description=description,
            status=status,
            tech_stack=tech_stack,
            estimated_hours=estimated_hours,
            repo_url=repo_url,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    update_project(session, project, project_data)
    return RedirectResponse(url=f"/projects/{project.id}", status_code=303)


@router.post("/projects/{project_id}/delete")
def project_delete(project_id: int, session: Session = Depends(get_session)):
    project = get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    delete_project(session, project)
    return RedirectResponse(url="/", status_code=303)
