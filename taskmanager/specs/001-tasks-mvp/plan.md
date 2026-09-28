# Plan técnico — MVP tasks-cli

Lee `docs/constitution.md` y `specs/001-tasks-mvp/spec.md`. Este plan es el cómo. Cada bloque indica qué requisitos cubre.

## Estructura de módulos

- `tasks/core.py` — lógica pura, sin entrada/salida ni disco. Cubre RF-1, RF-2, RF-4, RF-5, el efecto de borrado de RF-7 y los casos límite de longitud, duplicado con espacios y tarea ya completada.
- `tasks/storage.py` — lee y escribe el JSON. No parsea comandos ni imprime mensajes. Cubre RNF-1 y el caso límite de datos ilegibles.
- `tasks/cli.py` — única interfaz: interpreta la línea de comandos, formatea la tabla y los mensajes en español, y pide la confirmación. Cubre RF-3, RF-6, la pregunta de RF-7 y la presentación de RF-4.
- `tests/` — un test por regla de negocio, ejecutados con `pytest -q` (constitución, principio 4).

`core.py` devuelve datos o un error estructurado. Quien traduce ese error a una frase en español es `cli.py`.

## Modelo de datos JSON

El almacén es el fichero `tasks.json` en el directorio de trabajo. Cubre RNF-1.

```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Comprar leche",
      "status": "pending",
      "created_at": "28-09-2026 14:00",
      "completed_at": null
    },
    {
      "id": 2,
      "description": "Enviar la práctica",
      "status": "completed",
      "created_at": "28-09-2026 09:15",
      "completed_at": "28-09-2026 11:40"
    }
  ]
}
```

- `status` solo admite `pending` o `completed` (RF-1, RF-5).
- `description` es el texto ya recortado, de 1 a 80 caracteres (RF-1, RF-2).
- `created_at` y `completed_at` usan `dd-mm-yyyy hh:mm`. `completed_at` es `null` mientras la tarea está `pending`.
- `id` es un entero. El siguiente es `max(id) + 1`, o `1` si no hay tareas. No se rellena el hueco de un id borrado (RF-1).

## Algoritmo de filtrado y ordenación

Cubre RF-3 (orden) y RF-4 (filtro y valor por defecto).

```text
función filtrar_y_ordenar(tareas, filtro):
    si filtro es nulo o "pendientes":
        resultado ← tareas cuyo status es "pending"
    si no, si filtro es "completadas":
        resultado ← tareas cuyo status es "completed"
    si no, si filtro es "todas":
        resultado ← copia de tareas
    si no:
        devolver error de filtro no válido
    ordenar resultado por id ascendente
    devolver resultado

función nuevo_id(tareas):
    si tareas está vacía:
        devolver 1
    devolver máximo de id + 1
```

## Contrato de la CLI

Entrada: `python -m tasks <comando>`. Cubre RF-1 a RF-7 en la interfaz.

Comandos:

- `add <descripción>` — crea una tarea (RF-1, RF-2 y el límite de longitud).
- `list [--filter pendientes|completadas|todas]` — lista tareas. Sin `--filter`, solo pendientes (RF-3, RF-4).
- `done <id>` — completa una tarea (RF-5, RF-6 y el caso de ya completada).
- `remove <id>` — pide confirmación y, si procede, elimina (RF-6, RF-7).

Salidas correctas (código 0):

- Crear: `Tarea <id> creada.`
- Listar: tabla con cabecera `ID  Descripción  Estado  Creada  Completada` y una fila por tarea. Sin filas, solo la cabecera.
- Completar: `Tarea <id> completada.`
- Borrar, tras responder `S`: `Tarea <id> eliminada.`
- Borrar cancelado: pregunta `¿Estás seguro? (S/N)` y después `Operación cancelada.`

Salidas de error de uso o de negocio (código 1):

- `Error: La descripción debe tener entre 1 y 80 caracteres`
- `Error: Ya existe una tarea con esa descripción`
- `Error: El ID <id> no existe`
- `Error: La tarea <id> ya está completada`
- `Error: Filtro no válido. Use pendientes, completadas o todas.`
- Faltan argumentos: el mensaje de uso del comando, en español.

Almacén ilegible (código 2):

- `Error: No se pueden leer las tareas guardadas`
- El fichero no se sustituye por uno vacío.

## Decisiones técnicas

1. **Módulo `storage.py` aparte de la CLI.** Así `core.py` sigue sin disco y `cli.py` solo parsea y formatea (constitución, principio 3). Alternativa descartada: leer y escribir el JSON dentro de `cli.py`. Esa opción mezcla persistencia con textos de la interfaz y complica los tests de RNF-1.
2. **`tasks.json` en el directorio de trabajo.** Un junior puede abrir el fichero junto al comando. Alternativa descartada: un fichero oculto en el directorio personal. Cuesta más de inspeccionar en un ejercicio. Cubre RNF-1.
3. **`argparse` de la biblioteca estándar** para los cuatro comandos. Alternativa descartada: interpretar `sys.argv` a mano. Hay más código propio y es más fácil olvidar un caso de uso. Cubre el contrato de la CLI.
4. **El id nuevo es `max(id) + 1`.** Un identificador borrado no reaparece. Alternativa descartada: reutilizar el primer hueco. Confunde una tarea nueva con una ya eliminada. Cubre RF-1.
5. **Python 3.10+ y biblioteca estándar.** `pytest` es la única dependencia, y solo para tests, porque la constitución exige `pytest -q` (principio 4) y prohíbe otras dependencias (principio 1). Alternativa descartada: añadir un formateador o una librería de tablas. No hace falta para el MVP.

## Estrategia de tests

Comando: `pytest -q`. Mínimo un test por RF, escrito antes que la lógica que lo cubre.

- RF-1: descripción válida; id 1 y luego `max + 1` aunque se haya borrado un id intermedio; `created_at` con el formato de la spec; estado `pending`.
- RF-1 (límite): vacía, solo espacios y más de 80 caracteres no se guardan.
- RF-2: duplicado exacto y duplicado con espacios alrededor; «Comprar» y «comprar» sí se permiten.
- RF-3: la tabla usa «pendiente» y «completada»; `completed_at` nulo sale en blanco; sin filas hay cabecera y código 0.
- RF-4: `pendientes`, `completadas`, `todas` y el filtro ausente; el orden es por id ascendente; un filtro desconocido da código 1.
- RF-5: un id `pending` pasa a `completed` y guarda la fecha de cierre.
- Caso de RF-5: completar una tarea ya `completed` no cambia la fecha y da código 1.
- RF-6: id ausente o no entero en `done` y en `remove`; el mensaje es `Error: El ID <id> no existe` y los datos no cambian.
- RF-7: solo la respuesta `S` borra; `s`, `N` y una línea vacía imprimen `Operación cancelada.` y devuelven código 0.
- RNF-1: ida y vuelta de `load`/`save` con el ejemplo de este plan; un JSON ilegible devuelve código 2 y deja el fichero como estaba.
