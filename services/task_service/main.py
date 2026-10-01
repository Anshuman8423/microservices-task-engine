from datetime import datetime, timezone
from typing import Dict
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Microservices Task Engine",
    description="Task management microservice for distributed task processing",
    version="1.0.0",
)


tasks: Dict[str, dict] = {}


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: str = "normal"


class TaskStatusUpdate(BaseModel):
    status: str


@app.get("/")
def root():
    return {
        "service": "task-service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "service": "task-service",
        "status": "healthy"
    }


@app.post("/tasks", status_code=201)
def create_task(request: TaskCreate):
    task_id = str(uuid4())

    task = {
        "task_id": task_id,
        "title": request.title,
        "description": request.description,
        "priority": request.priority,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    tasks[task_id] = task

    return {
        "success": True,
        "task": task
    }


@app.get("/tasks")
def get_tasks():
    return {
        "success": True,
        "count": len(tasks),
        "tasks": list(tasks.values())
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "success": True,
        "task": task
    }


@app.patch("/tasks/{task_id}/status")
def update_task_status(
    task_id: str,
    request: TaskStatusUpdate
):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task["status"] = request.status

    return {
        "success": True,
        "task": task
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = tasks.pop(task_id)

    return {
        "success": True,
        "deleted_task": deleted_task
    }