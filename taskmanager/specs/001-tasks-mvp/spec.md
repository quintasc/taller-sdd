# Spec 001 — MVP de gestión de tareas

## Contexto y objetivo
Una persona que trabaja en la terminal necesita anotar tareas, ver cuáles siguen abiertas, marcarlas al terminarlas y borrarlas si ya no aplican. Esta primera versión resuelve ese flujo con persistencia local y un comportamiento lo bastante pequeño para que lo mantenga un desarrollador junior.

## Usuarios / actores
- Usuario de terminal: crea, consulta, completa y elimina sus tareas.
- Desarrollador junior: mantiene el producto a partir de esta spec y del plan.

## Historias de usuario
- H1: Como usuario de terminal quiero crear una tarea con una descripción breve para no olvidar lo que tengo pendiente.
- H2: Como usuario de terminal quiero listar las tareas pendientes, las completadas o todas para ver en qué estado está cada una.
- H3: Como usuario de terminal quiero marcar una tarea como completada mediante su identificador para dejar constancia de que ya está hecha.
- H4: Como usuario de terminal quiero eliminar una tarea solo después de confirmarlo para no borrarla por accidente.

## Requisitos funcionales (criterios de aceptación en EARS)
- RF-1: CUANDO el usuario pide crear una tarea cuya descripción, tras quitar espacios al inicio y al final, tiene entre 1 y 80 caracteres y no coincide con ninguna existente, EL SISTEMA guarda esa descripción recortada, le asigna un identificador entero (el primero es 1 y el siguiente es el máximo existente más uno, sin reutilizar identificadores borrados), la deja en estado `pending` y registra la fecha de creación en formato `dd-mm-yyyy hh:mm` (hora en 24 h, con dos dígitos).
- RF-2: SI el usuario intenta crear una tarea cuya descripción recortada es idéntica, respetando mayúsculas y minúsculas, a la de una tarea ya existente, ENTONCES EL SISTEMA muestra «Error: Ya existe una tarea con esa descripción» y no guarda la tarea.
- RF-3: EL SISTEMA muestra el listado en una tabla con identificador, descripción, estado, fecha de creación y fecha de completado, ordenada por identificador ascendente. El estado `pending` se muestra como «pendiente» y el estado `completed` como «completada». Si no hay fecha de completado, esa celda queda vacía.
- RF-4: CUANDO el usuario solicita listar, EL SISTEMA filtra por `pendientes` (estado `pending`), `completadas` (estado `completed`) o `todas`. SI el usuario no indica filtro, ENTONCES EL SISTEMA muestra solo las pendientes.
- RF-5: CUANDO el usuario pide completar un identificador que existe y la tarea está `pending`, EL SISTEMA la pasa a `completed` y registra la fecha y hora de cierre en formato `dd-mm-yyyy hh:mm`.
- RF-6: SI el usuario intenta completar o eliminar un identificador que no existe o que no es un entero, ENTONCES EL SISTEMA muestra «Error: El ID <id> no existe» (con el texto indicado por el usuario en lugar de `<id>`) y no modifica los datos.
- RF-7: CUANDO el usuario solicita borrar una tarea cuyo identificador existe, EL SISTEMA pregunta «¿Estás seguro? (S/N)». SI la respuesta es exactamente «S», ENTONCES EL SISTEMA elimina la tarea. SI la respuesta es cualquier otra, incluidas «s» y «N», ENTONCES EL SISTEMA no elimina la tarea e informa de que la operación se ha cancelado.

## Requisitos no funcionales
- RNF-1: Los datos se conservan entre ejecuciones en un JSON plano local. El esquema concreto está en el plan. Sin base de datos, sin red y sin formatos binarios.
- RNF-2: Los mensajes de la interfaz están en español. El código y la documentación técnica están en inglés.

## Casos límite
- Descripción vacía, solo espacios, o de más de 80 caracteres tras recortar: EL SISTEMA muestra «Error: La descripción debe tener entre 1 y 80 caracteres» y no guarda la tarea (RF-1).
- La misma descripción con espacios al inicio o al final cuenta como duplicado (RF-2). «Comprar» y «comprar» son descripciones distintas.
- Completar una tarea que ya está `completed`: EL SISTEMA muestra «Error: La tarea <id> ya está completada» y no cambia la fecha de cierre.
- Confirmación distinta de «S»: no se borra nada (RF-7).
- Listado sin filas (no hay tareas o el filtro no devuelve ninguna): EL SISTEMA muestra la cabecera y ninguna fila, y no lo trata como error (RF-3, RF-4).
- Datos guardados ilegibles o corruptos: EL SISTEMA muestra «Error: No se pueden leer las tareas guardadas» y no sustituye el almacén por uno vacío (RNF-1).
- Identificador ausente o no entero: se aplica RF-6.

## Fuera de alcance
- Editar la descripción de una tarea ya creada.
- Fecha límite, prioridad, etiquetas o subtareas.
- Reabrir una tarea completada.
- Varios usuarios, varios almacenes o sincronización.
- Deshacer un borrado.
- Interfaz gráfica.

## Criterios de finalización
- Cada requisito RF-1 a RF-7 tiene al menos un test automático en verde.
- Hay una demostración manual del flujo principal: crear una tarea, listar pendientes y todas, completarla, intentar borrarla con una respuesta distinta de «S» y borrarla confirmando con «S».

## Dudas abiertas
- Ninguna. No queda ningún punto marcado como [NECESITA ACLARACIÓN]. Quedan cerrados el vocabulario de estado (`pending` / `completed`, con etiquetas en español en la salida), el filtro por defecto (pendientes), la confirmación solo con «S» exacta, los duplicados tras recortar espacios y los identificadores que no se reutilizan.
