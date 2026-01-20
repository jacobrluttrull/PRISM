# PRISM Project Context

## What is PRISM?
PRISM (Project Repo Intelligence & Setup Manager) is a Windows-first FastAPI web application that acts as a personal developer portal for my local repositories.

It lets me:
- Register local project folders by path
- View a dashboard of projects
- Run common workflows (format/lint/test/build) from a web UI
- Store and display results (exit code, output logs, timestamps)

PRISM is designed to reduce setup friction and wasted time when working across multiple projects.

---

## Goals
- Be useful daily (developer productivity tool)
- Clean modular architecture (routers/services/db/core)
- Minimal UI complexity (Jinja2 templates, no React)
- Strong engineering practices (ruff, pytest, clean error handling)
- Safe and reliable subprocess execution on Windows

---

## Non-goals (for now)
- No cloud deployment required
- No GitHub API integration required
- No heavy frontend frameworks
- No Docker required

---

## Tech Stack
- Python 3.x (Windows / PowerShell)
- FastAPI
- Jinja2 templates
- SQLModel + SQLite (PostgreSQL later if needed)
- Uvicorn
- Ruff + Pytest

---

## Core Features (MVP)
- Home page lists registered projects
- Add project form (name + local path)
- Project detail page

---

## Planned Features
- Run workflow buttons:
  - Format (ruff format)
  - Lint (ruff check)
  - Tests (python -m pytest)
- Store job run history per project
- Show last run status + output logs in the UI
- Optional: profiles per project type (python, django, fastapi, etc.)

---

## Key Constraints
- Must support Windows paths (including spaces)
- Prefer `python -m ...` command style for reliability
- Avoid Unix-only assumptions
- Build incrementally with small milestones

---

## Notes for AI/Codex
When adding features:
- Keep changes small and testable
- Prefer service-layer functions over logic in route handlers
- Capture subprocess stdout/stderr and exit codes
- Never run destructive commands automatically without a confirmation step

