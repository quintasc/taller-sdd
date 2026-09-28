# Tareas de implementación — MVP tasks-cli

Orden de dependencia. Cada tarea cabe en 20-30 minutos. En las de lógica, los tests se escriben antes que el código. No se empieza la siguiente hasta cumplir su «Hecho cuando».

- [x] **T1. Estructura del paquete** (~20 min). RF: ninguno; deja el esqueleto que exige el plan.
  Hecho cuando: existen `tasks/__init__.py`, `tasks/core.py`, `tasks/storage.py`, `tasks/cli.py` y `tests/`, y `pytest -q` termina sin errores de recolección.

- [x] **T2. Creación válida** (~25 min). RF-1.
  Hecho cuando: hay tests previos de descripción válida, id incremental y fecha de creación; `pytest -q` los pasa, y la tarea queda `pending` con `created_at` en formato `dd-mm-yyyy hh:mm`.

- [x] **T3. Duplicados** (~20 min). RF-2.
  Hecho cuando: un duplicado exacto y uno con espacios alrededor no se guardan, «Comprar» y «comprar» sí pueden coexistir, y `pytest -q` pasa.

- [x] **T4. Longitud de la descripción** (~20 min). Caso límite de RF-1.
  Hecho cuando: la descripción vacía, la de solo espacios y la de más de 80 caracteres no se guardan, y `pytest -q` pasa.

- [x] **T5. Filtro y orden** (~25 min). RF-4 y el orden de RF-3.
  Hecho cuando: `pendientes`, `completadas`, `todas` y el filtro ausente devuelven el subconjunto de la spec, ordenado por id ascendente, y `pytest -q` pasa.

- [x] **T6. Completar** (~25 min). RF-5 y el caso de tarea ya completada.
  Hecho cuando: un id `pending` pasa a `completed` con fecha de cierre; repetir la operación no cambia esa fecha, y `pytest -q` pasa.

- [x] **T7. Borrado en la lógica** (~20 min). Efecto de RF-7 y el id inexistente de RF-6, todavía sin textos de la interfaz.
  Hecho cuando: borrar un id existente lo quita de la lista; borrar un id ausente deja la lista igual y devuelve error, y `pytest -q` pasa.

- [x] **T8. Persistencia** (~25 min). RNF-1 y el caso de JSON ilegible.
  Hecho cuando: guardar y volver a cargar reproduce el ejemplo del plan; un JSON ilegible produce error y no sustituye el fichero por uno vacío, y `pytest -q` pasa.

- [x] **T9. CLI crear** (~25 min). RF-1 y RF-2 en la interfaz.
  Hecho cuando: `add` imprime `Tarea <id> creada.` con código 0, o el error de duplicado o de longitud con código 1, y `pytest -q` pasa.

- [x] **T10. CLI listar** (~30 min). RF-3 y RF-4.
  Hecho cuando: la tabla muestra las cinco columnas y las etiquetas «pendiente» y «completada»; sin `--filter` salen solo las pendientes; un listado vacío devuelve código 0, y `pytest -q` pasa.

- [x] **T11. CLI completar** (~25 min). RF-5 y RF-6.
  Hecho cuando: `done` imprime `Tarea <id> completada.` o `Error: El ID <id> no existe` o `Error: La tarea <id> ya está completada`, con el código de salida del plan, y `pytest -q` pasa.

- [x] **T12. CLI eliminar** (~25 min). RF-7 y RF-6.
  Hecho cuando: se pregunta «¿Estás seguro? (S/N)»; solo «S» borra; cualquier otra respuesta imprime `Operación cancelada.` y devuelve código 0; un id inexistente usa el mensaje de RF-6, y `pytest -q` pasa.

- [x] **T13. Verificación final** (~20 min). RF-1 a RF-7 y los criterios de finalización de la spec.
  Hecho cuando: `pytest -q` pasa entero y queda anotada la demo manual: crear, listar pendientes y todas, completar, cancelar un borrado y borrar confirmando con «S».
  Demo (28-09-2026): `pytest -q` con 19 tests en verde. Flujo manual: crear las tareas 1 y 2, listar pendientes y todas, completar la 1, cancelar el borrado con N (salida 0) y borrarla con S. Quedó la tarea 2.
