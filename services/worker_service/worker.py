import time
from datetime import datetime, timezone


def process_task(task: dict) -> dict:
    """
    Process a single task.

    In a production system, this function would perform
    the actual background task processing.
    """

    task_id = task["task_id"]
    title = task["title"]

    print(
        f"[{datetime.now(timezone.utc).isoformat()}] "
        f"Processing task {task_id}: {title}"
    )

    # Simulate background processing
    time.sleep(1)

    result = {
        "task_id": task_id,
        "status": "completed",
        "message": f"Task '{title}' processed successfully",
    }

    print(
        f"[{datetime.now(timezone.utc).isoformat()}] "
        f"Task {task_id} completed"
    )

    return result


if __name__ == "__main__":
    demo_task = {
        "task_id": "demo-task-001",
        "title": "Demo Task",
        "description": "Test background task",
        "priority": "normal",
    }

    result = process_task(demo_task)

    print(result)