# AGENTS.md — tasks-cli

## Proyecto
CLI en Python para gestionar tareas personales: crear, listar, completar y eliminar. La lógica vive en `tasks/core.py` (sin entrada/salida), la persistencia en `tasks/storage.py` (JSON local) y la interfaz en `tasks/cli.py` (solo parsea y formatea). Está pensada para que la mantenga un desarrollador junior.

## Comandos
- Ejecutar: `python -m tasks <comando>`
- Tests: `pytest -q`
- Lint/formato: `python -m compileall tasks tests` (comprueba la sintaxis; no hay formateador externo)

## Estilo y convenciones
- Python 3.10+ y biblioteca estándar. `pytest` es la única dependencia, y solo para tests.
- Type hints en las funciones públicas. Identificadores y docstrings en inglés. Mensajes de usuario en español.
- El esquema JSON está en `specs/001-tasks-mvp/plan.md`.

## Reglas
- Lee `docs/constitution.md` y la spec activa en `specs/` antes de tocar código.
- No añadas dependencias ni cambies el formato del JSON sin actualizar antes el plan.
- No modifiques archivos dentro de `specs/` salvo petición explícita.

## Al terminar cualquier tarea
- Ejecuta `pytest -q` y confirma en tu respuesta que todo pasa.
