"""Read and write the local JSON store. No user-facing text."""

import json
from pathlib import Path

from tasks.core import Task

_TASK_FIELDS = {"id", "description", "status", "created_at", "completed_at"}


class StorageError(Exception):
    """The store cannot be read. Callers must not overwrite it."""


def load_tasks(path: Path) -> list[Task]:
    """Return the tasks in ``path``. A missing file is an empty list."""
    if not path.exists():
        return []
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StorageError("unreadable store") from exc
    tasks = data.get("tasks") if isinstance(data, dict) else None
    if not isinstance(tasks, list) or any(not _is_task(item) for item in tasks):
        raise StorageError("unreadable store")
    return tasks


def save_tasks(path: Path, tasks: list[Task]) -> None:
    """Replace ``path`` with the given tasks."""
    text = json.dumps({"tasks": tasks}, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def _is_task(item: object) -> bool:
    return isinstance(item, dict) and _TASK_FIELDS <= item.keys()
