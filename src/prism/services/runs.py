from models import JobRun
from models import Project
from sqlmodel import Session, select
from datetime import datetime, timezone



def create_run(
        session: Session,
        project_id: int,
        command: str,
        job_type: str,
        cwd: str,
        created_at: datetime,
) -> JobRun:
    run = JobRun(
        project_id=project_id,
        command=command,
        job_type=job_type,
        cwd=cwd,
        started_at=created_at.isoformat(),
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def mark_finished(
    session: Session,
    run_id: int,
    exit_code: int,
    stdout: str,
    stderr: str,
    error_message: str | None = None,
) -> JobRun:
    run = session.get(JobRun, run_id)
    if not run:
        raise ValueError("Run not found.")

    finished_at = datetime.now(timezone.utc)

    duration_ms = None
    if run.created_at:
        duration_ms = int((finished_at - run.created_at).total_seconds() * 1000)

    run.finished_at = finished_at
    run.exit_code = exit_code
    run.stdout = stdout
    run.stderr = stderr
    run.error_message = error_message
    run.status = "success" if exit_code == 0 else "failed"
    run.duration_ms = duration_ms

    session.add(run)
    session.commit()
    session.refresh(run)
    return run

def mark_running(session: Session, run_id: int) -> JobRun:
    run = session.get(JobRun, run_id)
    if not run:
        raise ValueError("Run not found.")

    run.status = "running"
    session.add(run)
    session.commit()
    session.refresh(run)
    return run

def get_latest_run(session: Session, project_id: int, job_type: str | None = None) -> JobRun | None:
    query = select(JobRun).where(JobRun.project_id == project_id)
    if job_type:
        query = query.where(JobRun.job_type == job_type)
    query = query.order_by(JobRun.started_at.desc())
    result = session.exec(query).first()
    return result

def list_runs(session: Session, project_id: int, limit: int = 20, job_type: str | None = None) -> list[JobRun]:
    query = select(JobRun).where(JobRun.project_id == project_id)
    if job_type:
        query = query.where(JobRun.job_type == job_type)
    query = query.order_by(JobRun.started_at.desc()).limit(limit)
    results = session.exec(query).all()
    return results
