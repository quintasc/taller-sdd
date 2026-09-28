# Taller SDD: una CLI para gestionar tareas

Proyecto educativo de desarrollo dirigido por especificación. La carpeta `samples` trae las plantillas y los prompts. `taskmanager` es la CLI en Python: crear, listar, completar y eliminar tareas, con los datos en un JSON local.

## Camino rápido

Entra en `taskmanager` y ejecuta:

1. `python -m tasks add "Comprar leche"`
2. `python -m tasks list`
3. `pytest -q`

Si el alta funciona, la primera orden imprime `Tarea 1 creada.` Los tests tienen que terminar en verde.

## Comandos

Ejecuta estos comandos desde `taskmanager`.

| Acción | Comando |
| --- | --- |
| Crear | `python -m tasks add "Comprar leche"` |
| Listar pendientes | `python -m tasks list` |
| Listar todas | `python -m tasks list --filter todas` |
| Listar completadas | `python -m tasks list --filter completadas` |
| Completar | `python -m tasks done 1` |
| Eliminar | `python -m tasks remove 1` |
| Tests | `pytest -q` |
| Sintaxis | `python -m compileall tasks tests` |

Al eliminar, la CLI pregunta `¿Estás seguro? (S/N)`. Solo la respuesta `S` borra la tarea. El identificador es el de la columna `ID`.

Las tareas se guardan en `tasks.json`, en el directorio desde el que lanzas el comando. Ese fichero no se versiona.

## Qué hay en el repositorio

| Ruta | Contenido |
| --- | --- |
| `samples/` | Prompts del taller y plantillas de `AGENTS.md` y `spec.md` |
| `taskmanager/docs/constitution.md` | Seis principios del proyecto |
| `taskmanager/specs/001-tasks-mvp/` | Spec, plan y tareas del MVP |
| `taskmanager/tasks/` | Código: lógica, persistencia y CLI |
| `taskmanager/tests/` | Tests de cada requisito |

Python 3.10+ y biblioteca estándar. La única dependencia externa es `pytest`, y solo para los tests.

## Comprobación

- [ ] `python -m tasks add "Comprar leche"` crea la tarea 1.
- [ ] `python -m tasks list` muestra la cabecera y esa tarea como pendiente.
- [ ] `python -m tasks done 1` la marca como completada.
- [ ] `pytest -q` pasa.

## Siguiente paso

Lee los prompts en [`samples/PromptsSDD.md`](samples/PromptsSDD.md) y la spec activa en [`taskmanager/specs/001-tasks-mvp/spec.md`](taskmanager/specs/001-tasks-mvp/spec.md).
