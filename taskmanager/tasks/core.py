"""Pure task rules. No input, output, or disk access."""

from datetime import datetime
from typing import TypedDict


class Task(TypedDict):
    """One stored task."""

    id: int
    description: str
    status: str
    created_at: str
    completed_at: str | None


class CoreError(Exception):
    """Domain error. The CLI turns ``code`` into a Spanish message."""

    def __init__(self, code: str, task_id: int | str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.task_id = task_id


def format_timestamp(moment: datetime) -> str:
    """Format a moment as dd-mm-yyyy hh:mm."""
    return moment.strftime("%d-%m-%Y %H:%M")


def new_id(tasks: list[Task]) -> int:
    """Return 1 when there are no tasks, otherwise one past the highest id."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(tasks: list[Task], description: str, now: datetime) -> list[Task]:
    """Append a pending task, or raise CoreError without changing ``tasks``."""
    cleaned = description.strip()
    if not 1 <= len(cleaned) <= 80:
        raise CoreError("invalid_description")
    if any(task["description"] == cleaned for task in tasks):
        raise CoreError("duplicate")
    created: Task = {
        "id": new_id(tasks),
        "description": cleaned,
        "status": "pending",
        "created_at": format_timestamp(now),
        "completed_at": None,
    }
    return [*tasks, created]


def filter_and_sort(tasks: list[Task], task_filter: str | None) -> list[Task]:
    """Keep pending, completed, or every task, then sort by id."""
    if task_filter is None or task_filter == "pendientes":
        selected = [task for task in tasks if task["status"] == "pending"]
    elif task_filter == "completadas":
        selected = [task for task in tasks if task["status"] == "completed"]
    elif task_filter == "todas":
        selected = list(tasks)
    else:
        raise CoreError("invalid_filter")
    return sorted(selected, key=lambda task: task["id"])


def complete_task(tasks: list[Task], task_id: int, now: datetime) -> list[Task]:
    """Mark a pending task completed. Leave ``tasks`` unchanged on error."""
    current = _find(tasks, task_id)
    if current["status"] == "completed":
        raise CoreError("already_completed", task_id=task_id)
    closed = format_timestamp(now)
    return [
        {**task, "status": "completed", "completed_at": closed}
        if task["id"] == task_id
        else task
        for task in tasks
    ]


def delete_task(tasks: list[Task], task_id: int) -> list[Task]:
    """Remove the task with ``task_id``. Raise CoreError if it is absent."""
    _find(tasks, task_id)
    return [task for task in tasks if task["id"] != task_id]


def _find(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise CoreError("not_found", task_id=task_id)
