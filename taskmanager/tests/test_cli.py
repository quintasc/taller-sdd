"""Spanish CLI contract: messages and exit codes."""

from datetime import datetime

from tasks.cli import HEADER, main
from tasks.storage import load_tasks, save_tasks

NOW = datetime(2026, 9, 28, 14, 0)
LATER = datetime(2026, 9, 28, 18, 30)


def test_add_prints_created_message(capsys, tmp_path):
    path = tmp_path / "tasks.json"
    code = main(["add", "Comprar", "leche"], store_path=path, now=NOW)
    assert code == 0
    assert capsys.readouterr().out.strip() == "Tarea 1 creada."
    assert load_tasks(path)[0]["description"] == "Comprar leche"
    assert load_tasks(path)[0]["status"] == "pending"


def test_add_duplicate_and_invalid_length_exit_1(capsys, tmp_path):
    path = tmp_path / "tasks.json"
    main(["add", "Comprar"], store_path=path, now=NOW)
    capsys.readouterr()

    duplicate = main(["add", "  Comprar  "], store_path=path, now=NOW)
    assert duplicate == 1
    assert capsys.readouterr().out.strip() == "Error: Ya existe una tarea con esa descripción"
    assert len(load_tasks(path)) == 1

    too_long = main(["add", "a" * 81], store_path=path, now=NOW)
    assert too_long == 1
    assert (
        capsys.readouterr().out.strip()
        == "Error: La descripción debe tener entre 1 y 80 caracteres"
    )
    assert len(load_tasks(path)) == 1


def test_list_columns_labels_default_filter_and_empty(capsys, tmp_path):
    path = tmp_path / "tasks.json"
    empty = main(["list"], store_path=path)
    empty_out = capsys.readouterr().out
    assert empty == 0
    assert empty_out.strip() == HEADER
    assert not path.exists()

    save_tasks(
        path,
        [
            _task(2, "Cerrada", "completed", "28-09-2026 11:40"),
            _task(1, "Abierta", "pending"),
        ],
    )
    default = main(["list"], store_path=path)
    default_out = capsys.readouterr().out
    assert default == 0
    assert default_out.splitlines()[0].split("  ") == [
        "ID",
        "Descripción",
        "Estado",
        "Creada",
        "Completada",
    ]
    assert "pendiente" in default_out
    assert "Abierta" in default_out
    assert "Cerrada" not in default_out

    all_rows = main(["list", "--filter", "todas"], store_path=path)
    listed = capsys.readouterr().out
    assert all_rows == 0
    assert "completada" in listed
    assert "28-09-2026 11:40" in listed
    ids = [line.split("  ", 1)[0] for line in listed.splitlines()[1:]]
    assert ids == ["1", "2"]

    invalid = main(["list", "--filter", "todo"], store_path=path)
    assert invalid == 1
    assert (
        capsys.readouterr().out.strip()
        == "Error: Filtro no válido. Use pendientes, completadas o todas."
    )


def test_done_completes_or_reports_id_and_already_done(capsys, tmp_path):
    path = tmp_path / "tasks.json"
    main(["add", "Comprar"], store_path=path, now=NOW)
    capsys.readouterr()

    missing = main(["done", "9"], store_path=path, now=LATER)
    assert missing == 1
    assert capsys.readouterr().out.strip() == "Error: El ID 9 no existe"
    assert load_tasks(path)[0]["status"] == "pending"

    text_id = main(["done", "abc"], store_path=path, now=LATER)
    assert text_id == 1
    assert capsys.readouterr().out.strip() == "Error: El ID abc no existe"

    done = main(["done", "1"], store_path=path, now=LATER)
    assert done == 0
    assert capsys.readouterr().out.strip() == "Tarea 1 completada."
    stored = load_tasks(path)[0]
    assert stored["status"] == "completed"
    assert stored["completed_at"] == "28-09-2026 18:30"

    again = main(["done", "1"], store_path=path, now=datetime(2026, 9, 29, 8, 0))
    assert again == 1
    assert capsys.readouterr().out.strip() == "Error: La tarea 1 ya está completada"
    assert load_tasks(path)[0]["completed_at"] == "28-09-2026 18:30"


def test_remove_confirms_and_rejects_unknown_id(capsys, tmp_path):
    path = tmp_path / "tasks.json"
    main(["add", "Comprar"], store_path=path, now=NOW)
    main(["add", "Otra"], store_path=path, now=NOW)
    capsys.readouterr()

    missing = main(["remove", "abc"], store_path=path, read_confirmation=lambda: "S")
    assert missing == 1
    assert capsys.readouterr().out.strip() == "Error: El ID abc no existe"
    assert len(load_tasks(path)) == 2

    cancelled = main(["remove", "1"], store_path=path, read_confirmation=lambda: "N")
    cancelled_out = capsys.readouterr().out
    assert cancelled == 0
    assert cancelled_out.index("¿Estás seguro? (S/N)") < cancelled_out.index(
        "Operación cancelada."
    )
    assert len(load_tasks(path)) == 2

    lowercase = main(["remove", "1"], store_path=path, read_confirmation=lambda: "s")
    assert lowercase == 0
    assert "Operación cancelada." in capsys.readouterr().out
    blank = main(["remove", "1"], store_path=path, read_confirmation=lambda: "")
    assert blank == 0
    assert "Operación cancelada." in capsys.readouterr().out
    assert len(load_tasks(path)) == 2

    removed = main(["remove", "1"], store_path=path, read_confirmation=lambda: "S")
    assert removed == 0
    assert "Tarea 1 eliminada." in capsys.readouterr().out
    assert [task["id"] for task in load_tasks(path)] == [2]


def test_unreadable_store_exits_2_without_replacing_the_file(capsys, tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("{", encoding="utf-8")
    code = main(["list"], store_path=path)
    assert code == 2
    assert capsys.readouterr().out.strip() == "Error: No se pueden leer las tareas guardadas"
    assert path.read_text(encoding="utf-8") == "{"


def test_missing_command_exits_1(capsys):
    code = main([])
    captured = capsys.readouterr()
    assert code == 1
    assert "Gestiona tareas personales." in captured.err


def _task(task_id, description, status, completed_at=None):
    return {
        "id": task_id,
        "description": description,
        "status": status,
        "created_at": "28-09-2026 09:15",
        "completed_at": completed_at,
    }
