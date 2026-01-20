import pytest
from sqlmodel import SQLModel, Session, create_engine

from prism.services import projects


@pytest.fixture
def session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_normalize_project_inputs_success():
    data = projects.normalize_project_inputs(
        name="  PRISM  ",
        path="C:\\Projects\\PRISM",
        description="  Internal tool  ",
        status="Active",
        tech_stack="Python, FastAPI",
        estimated_hours="12",
        repo_url=" https://github.com/example/prism ",
    )

    assert data["name"] == "PRISM"
    assert data["path"] == "C:\\Projects\\PRISM"
    assert data["description"] == "Internal tool"
    assert data["status"] == "active"
    assert data["tech_stack"] == "Python, FastAPI"
    assert data["estimated_hours"] == 12
    assert data["repo_url"] == "https://github.com/example/prism"


def test_normalize_project_inputs_invalid_status():
    with pytest.raises(ValueError, match="Invalid status"):
        projects.normalize_project_inputs(
            name="PRISM",
            path="C:\\Projects\\PRISM",
            description=None,
            status="pending",
            tech_stack=None,
            estimated_hours=None,
            repo_url=None,
        )


def test_normalize_project_inputs_invalid_hours():
    with pytest.raises(ValueError, match="whole number"):
        projects.normalize_project_inputs(
            name="PRISM",
            path="C:\\Projects\\PRISM",
            description=None,
            status="active",
            tech_stack=None,
            estimated_hours="not-a-number",
            repo_url=None,
        )

    with pytest.raises(ValueError, match="cannot be negative"):
        projects.normalize_project_inputs(
            name="PRISM",
            path="C:\\Projects\\PRISM",
            description=None,
            status="active",
            tech_stack=None,
            estimated_hours="-1",
            repo_url=None,
        )


def test_create_update_delete_project(session):
    data = projects.normalize_project_inputs(
        name="PRISM",
        path="C:\\Projects\\PRISM",
        description="Initial",
        status="active",
        tech_stack="Python",
        estimated_hours="5",
        repo_url=None,
    )
    project = projects.create_project(session, data)
    assert project.id is not None

    fetched = projects.get_project(session, project.id)
    assert fetched is not None
    assert fetched.name == "PRISM"

    update = projects.normalize_project_inputs(
        name="PRISM v2",
        path="C:\\Projects\\PRISM",
        description="Updated",
        status="paused",
        tech_stack="Python, FastAPI",
        estimated_hours="8",
        repo_url="https://github.com/example/prism",
    )
    updated = projects.update_project(session, fetched, update)
    assert updated.name == "PRISM v2"
    assert updated.status == "paused"
    assert updated.estimated_hours == 8
    assert updated.repo_url == "https://github.com/example/prism"

    projects.delete_project(session, updated)
    assert projects.get_project(session, updated.id) is None
