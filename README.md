# PRISM MVP

Minimal FastAPI + Jinja2 app for registering local project paths and viewing them in a dashboard.

## Run (Windows PowerShell)

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install deps
python -m pip install -r requirements.txt

# Run the app
uvicorn prism.main:app --reload --app-dir src
```

The SQLite database file (`prism.db`) is created in the project root on first run.

## Migrations (Alembic)

```powershell
# Install Alembic
python -m pip install alembic

# Create your first migration
alembic revision --autogenerate -m "init"

# Apply migrations
alembic upgrade head
```

When you change models later, run another `alembic revision --autogenerate -m "..."` and then `alembic upgrade head`.

## Migration Workflow

```powershell
# After changing models
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

If a migration fails, check the generated file in `alembic/versions/` before retrying.

## PowerShell Shortcut

```powershell
.\scripts\migrate.ps1 "describe change"
```
