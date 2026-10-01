from fastapi.testclient import TestClient

from services.task_service.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "task-service"
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Build authentication service",
            "description": "Implement authentication",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["task"]["title"] == "Build authentication service"
    assert data["task"]["priority"] == "high"
    assert data["task"]["status"] == "pending"


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "tasks" in response.json()


def test_get_task_not_found():
    response = client.get("/tasks/non-existent-task")

    assert response.status_code == 404


def test_update_task_status():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test status update",
            "description": "Testing status",
            "priority": "normal",
        },
    )

    task_id = create_response.json()["task"]["task_id"]

    response = client.patch(
        f"/tasks/{task_id}/status",
        json={
            "status": "completed"
        },
    )

    assert response.status_code == 200
    assert response.json()["task"]["status"] == "completed"


def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "description": "Testing deletion",
            "priority": "low",
        },
    )

    task_id = create_response.json()["task"]["task_id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["success"] is True

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404