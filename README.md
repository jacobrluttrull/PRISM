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
