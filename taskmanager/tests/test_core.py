"""Business rules for creating, listing, completing, and deleting tasks."""

from datetime import datetime

import pytest

from tasks.core import (
    CoreError,
    add_task,
    complete_task,
    delete_task,
    filter_and_sort,
    format_timestamp,
)

NOW = datetime(2026, 9, 28, 14, 5)
LATER = datetime(2026, 9, 28, 16, 40)


def test_add_valid_task_is_pending_with_incremental_id_and_timestamp():
    created = add_task([], "  Comprar leche  ", NOW)
    assert created == [
        {
            "id": 1,
            "description": "Comprar leche",
            "status": "pending",
            "created_at": "28-09-2026 14:05",
            "completed_at": None,
        }
    ]
    assert format_timestamp(NOW) == "28-09-2026 14:05"

    again = add_task(created, "Enviar la práctica", NOW)
    assert [task["id"] for task in again] == [1, 2]
    assert again[1]["status"] == "pending"


def test_new_id_skips_deleted_identifiers():
    tasks = add_task([], "Una", NOW)
    tasks = add_task(tasks, "Dos", NOW)
    tasks = delete_task(tasks, 1)
    tasks = add_task(tasks, "Tres", NOW)
    assert [task["id"] for task in tasks] == [2, 3]


def test_duplicate_exact_and_trimmed_descriptions_are_rejected():
    tasks = add_task([], "Comprar leche", NOW)
    with pytest.raises(CoreError) as exact:
        add_task(tasks, "Comprar leche", NOW)
    assert exact.value.code == "duplicate"
    with pytest.raises(CoreError) as padded:
        add_task(tasks, "  Comprar leche  ", NOW)
    assert padded.value.code == "duplicate"
    assert len(tasks) == 1


def test_different_casing_is_not_a_duplicate():
    tasks = add_task([], "Comprar", NOW)
    tasks = add_task(tasks, "comprar", NOW)
    assert [task["description"] for task in tasks] == ["Comprar", "comprar"]


def test_empty_blank_and_too_long_descriptions_are_rejected():
    for description in ("", "   ", "a" * 81):
        with pytest.raises(CoreError) as exc:
            add_task([], description, NOW)
        assert exc.value.code == "invalid_description"
    created = add_task([], "a" * 80, NOW)
    assert created[0]["description"] == "a" * 80


def test_filter_and_default_sort_by_id():
    tasks = [
        _task(3, "Tres", "pending"),
        _task(1, "Una", "completed", "28-09-2026 11:40"),
        _task(2, "Dos", "pending"),
    ]
    assert [task["id"] for task in filter_and_sort(tasks, None)] == [2, 3]
    assert [task["id"] for task in filter_and_sort(tasks, "pendientes")] == [2, 3]
    assert [task["id"] for task in filter_and_sort(tasks, "completadas")] == [1]
    assert [task["id"] for task in filter_and_sort(tasks, "todas")] == [1, 2, 3]
    with pytest.raises(CoreError) as exc:
        filter_and_sort(tasks, "todo")
    assert exc.value.code == "invalid_filter"


def test_complete_pending_task_sets_status_and_timestamp():
    tasks = add_task([], "Comprar leche", NOW)
    done = complete_task(tasks, 1, LATER)
    assert done[0]["status"] == "completed"
    assert done[0]["completed_at"] == "28-09-2026 16:40"
    assert tasks[0]["status"] == "pending"


def test_completing_again_does_not_change_the_close_time():
    tasks = complete_task(add_task([], "Comprar leche", NOW), 1, LATER)
    with pytest.raises(CoreError) as exc:
        complete_task(tasks, 1, datetime(2026, 9, 29, 8, 0))
    assert exc.value.code == "already_completed"
    assert tasks[0]["completed_at"] == "28-09-2026 16:40"


def test_delete_removes_existing_id_and_rejects_a_missing_one():
    tasks = add_task([], "Comprar leche", NOW)
    tasks = add_task(tasks, "Otra", NOW)
    remaining = delete_task(tasks, 1)
    assert [task["id"] for task in remaining] == [2]
    with pytest.raises(CoreError) as exc:
        delete_task(remaining, 1)
    assert exc.value.code == "not_found"
    assert [task["id"] for task in remaining] == [2]


def _task(task_id: int, description: str, status: str, completed_at: str | None = None):
    return {
        "id": task_id,
        "description": description,
        "status": status,
        "created_at": "28-09-2026 09:15",
        "completed_at": completed_at,
    }
