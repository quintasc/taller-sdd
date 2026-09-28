"""JSON persistence."""

import pytest

from tasks.storage import StorageError, load_tasks, save_tasks

EXAMPLE = {
    "tasks": [
        {
            "id": 1,
            "description": "Comprar leche",
            "status": "pending",
            "created_at": "28-09-2026 14:00",
            "completed_at": None,
        },
        {
            "id": 2,
            "description": "Enviar la práctica",
            "status": "completed",
            "created_at": "28-09-2026 09:15",
            "completed_at": "28-09-2026 11:40",
        },
    ]
}


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "tasks.json"
    save_tasks(path, EXAMPLE["tasks"])
    assert load_tasks(path) == EXAMPLE["tasks"]


def test_missing_file_is_an_empty_list(tmp_path):
    assert load_tasks(tmp_path / "tasks.json") == []


def test_unreadable_json_raises_and_keeps_the_file(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(StorageError):
        load_tasks(path)
    assert path.read_text(encoding="utf-8") == "{"
