"""Command-line interface. Parses arguments and prints Spanish messages."""

import argparse
import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from tasks.core import CoreError, add_task, complete_task, delete_task, filter_and_sort
from tasks.storage import StorageError, load_tasks, save_tasks

HEADER = "ID  Descripción  Estado  Creada  Completada"
STORE_NAME = "tasks.json"


class TaskParser(argparse.ArgumentParser):
    """Parser that reports usage in Spanish and exits with code 1."""

    def error(self, message: str) -> None:
        self.print_help(sys.stderr)
        self.exit(1)


def build_parser() -> TaskParser:
    """Build the four-command parser."""
    parser = TaskParser(
        prog="tasks",
        description="Gestiona tareas personales.",
        usage="tasks <comando> [opciones]",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Crea una tarea.")
    add.add_argument("description", nargs="+", help="Descripción de la tarea.")

    listing = commands.add_parser("list", help="Lista las tareas.")
    listing.add_argument(
        "--filter",
        dest="task_filter",
        help="pendientes, completadas o todas. Por defecto: pendientes.",
    )

    done = commands.add_parser("done", help="Marca una tarea como completada.")
    done.add_argument("task_id", help="Identificador de la tarea.")

    remove = commands.add_parser("remove", help="Elimina una tarea.")
    remove.add_argument("task_id", help="Identificador de la tarea.")
    return parser


def main(
    argv: list[str] | None = None,
    *,
    store_path: Path | None = None,
    now: datetime | None = None,
    read_confirmation: Callable[[], str] | None = None,
) -> int:
    """Run one command and return its exit code."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 1

    path = store_path if store_path is not None else Path.cwd() / STORE_NAME
    moment = now if now is not None else datetime.now()
    try:
        tasks = load_tasks(path)
    except StorageError:
        print("Error: No se pueden leer las tareas guardadas")
        return 2

    if args.command == "add":
        return _add(path, tasks, " ".join(args.description), moment)
    if args.command == "list":
        return _list(tasks, args.task_filter)
    if args.command == "done":
        return _done(path, tasks, args.task_id, moment)
    return _remove(path, tasks, args.task_id, read_confirmation)


def format_table(tasks: list[dict]) -> str:
    """Render tasks with the five columns from the plan."""
    lines = [HEADER]
    for task in tasks:
        status = "pendiente" if task["status"] == "pending" else "completada"
        completed = task["completed_at"] or ""
        lines.append(
            "  ".join(
                [
                    str(task["id"]),
                    str(task["description"]),
                    status,
                    str(task["created_at"]),
                    completed,
                ]
            ).rstrip()
        )
    return "\n".join(lines)


def parse_task_id(raw: str) -> int | None:
    """Parse a decimal integer id. Return None when ``raw`` is not an integer."""
    text = raw.strip()
    if text.lstrip("-").isdigit() and text not in {"", "-"}:
        return int(text)
    return None


def _add(path: Path, tasks: list[dict], description: str, now: datetime) -> int:
    try:
        updated = add_task(tasks, description, now)
    except CoreError as exc:
        if exc.code == "duplicate":
            print("Error: Ya existe una tarea con esa descripción")
        else:
            print("Error: La descripción debe tener entre 1 y 80 caracteres")
        return 1
    save_tasks(path, updated)
    print(f"Tarea {updated[-1]['id']} creada.")
    return 0


def _list(tasks: list[dict], task_filter: str | None) -> int:
    try:
        selected = filter_and_sort(tasks, task_filter)
    except CoreError:
        print("Error: Filtro no válido. Use pendientes, completadas o todas.")
        return 1
    print(format_table(selected))
    return 0


def _done(path: Path, tasks: list[dict], raw_id: str, now: datetime) -> int:
    task_id = _existing_id(tasks, raw_id)
    if task_id is None:
        print(f"Error: El ID {raw_id} no existe")
        return 1
    try:
        updated = complete_task(tasks, task_id, now)
    except CoreError:
        print(f"Error: La tarea {task_id} ya está completada")
        return 1
    save_tasks(path, updated)
    print(f"Tarea {task_id} completada.")
    return 0


def _remove(
    path: Path,
    tasks: list[dict],
    raw_id: str,
    read_confirmation: Callable[[], str] | None,
) -> int:
    task_id = _existing_id(tasks, raw_id)
    if task_id is None:
        print(f"Error: El ID {raw_id} no existe")
        return 1
    print("¿Estás seguro? (S/N)")
    answer = (read_confirmation or input)()
    if answer != "S":
        print("Operación cancelada.")
        return 0
    updated = delete_task(tasks, task_id)
    save_tasks(path, updated)
    print(f"Tarea {task_id} eliminada.")
    return 0


def _existing_id(tasks: list[dict], raw_id: str) -> int | None:
    task_id = parse_task_id(raw_id)
    if task_id is None or not any(task["id"] == task_id for task in tasks):
        return None
    return task_id


if __name__ == "__main__":
    raise SystemExit(main())
