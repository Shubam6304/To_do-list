import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend import main
from backend.database import Base, get_db


@pytest.fixture()
def client(monkeypatch):
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    Base.metadata.create_all(bind=test_engine)
    monkeypatch.setattr(main, "engine", test_engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    with TestClient(main.app) as test_client:
        yield test_client
    main.app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_status_routes(client):
    root_response = client.get("/")
    assert root_response.status_code == 200
    assert root_response.json()["message"] == "To-Do List API is running"

    health_response = client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "healthy"


def test_task_crud(client):
    created = client.post(
        "/tasks",
        json={"title": "  Write tests  ", "description": "API coverage"},
    )
    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "Write tests"
    assert task["completed"] is False

    listing = client.get("/tasks")
    assert listing.status_code == 200
    assert [item["id"] for item in listing.json()] == [task["id"]]

    updated = client.put(f"/tasks/{task['id']}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    assert client.delete(f"/tasks/{task['id']}").status_code == 204
    assert client.get("/tasks").json() == []


def test_validation_and_missing_tasks(client):
    assert client.post("/tasks", json={"title": "   "}).status_code == 422
    assert client.post("/tasks", json={"title": "x" * 201}).status_code == 422
    assert client.put("/tasks/999", json={"title": None}).status_code == 422
    assert client.put("/tasks/999", json={"completed": True}).status_code == 404
    assert client.delete("/tasks/999").status_code == 404
