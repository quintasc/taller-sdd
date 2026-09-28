# Prompts SDD

## 1. Setup y Constitución

```text
Vamos a crear la constitución de un proyecto nuevo: una CLI en Python para
gestionar tareas (crear, listar, completar y eliminar). Es un proyecto educativo que
debe poder mantener un desarrollador junior.

Proponme un docs/constitution.md con 6 principios innegociables, cortos y
verificables, que cubran: simplicidad del stack, relación entre spec y código,
separación entre lógica e interfaz, política de tests, persistencia de datos
e idioma del código y los mensajes. Máximo 15 líneas. Espera mi aprobación.
```

*Genera el [/docs/constitution.md](./docs/constitution.md)*
*Escribimos el [AGENTS.md](./AGENTS.md) y el [CLAUDE.md](./CLAUDE.md)*

---

## 2. Especificación

```text
NO escribas código en ningún momento. Vamos a redactar la especificación de la
primera funcionalidad de tasks-cli. Lee docs/constitution.md.

Idea inicial: una CLI con cuatro comandos: crear una tarea, marcarla como completada, 
listar las tareas pendientes y eliminar una tarea.

Tu trabajo:
1. Hazme preguntas de UNA en UNA para eliminar ambigüedades (casos límite,
   comportamiento con errores, qué queda fuera del MVP). Máximo 6 preguntas.
2. Con mis respuestas, genera specs/001-tasks-mvp/spec.md con esta estructura:
   contexto y objetivo, usuarios, historias de usuario, requisitos funcionales
   numerados (RF-x) con criterios de aceptación en notación EARS en español,
   requisitos no funcionales, casos límite, fuera de alcance, criterios de
   finalización y dudas abiertas marcadas como [NECESITA ACLARACIÓN].
3. El QUÉ y el POR QUÉ. Nada de stack, arquitectura ni nombres de archivos:
   eso irá en el plan.
```

*Genera el [specs/001-tasks-mvp/spec.md](./specs/001-tasks-mvp/spec.md)*

---

## 3. Clarificación

```text
Revisa specs/001-tasks-mvp/spec.md como si fueras un QA muy profesional.
Lista: (1) ambigüedades restantes, (2) contradicciones entre requisitos,
(3) casos límite no cubiertos, (4) conflictos con docs/constitution.md.
No propongas soluciones todavía: solo detecta. Formato: lista numerada.
```

---

## 4. Planificación

```text
Lee docs/constitution.md y specs/001-tasks-mvp/spec.md. NO escribas código.
Genera specs/001-tasks-mvp/plan.md con: estructura de módulos, modelo de
datos JSON con un ejemplo, algoritmo de filtrado y ordenación de tareas en pseudocódigo,
contrato de la CLI (comandos, salidas, códigos de salida), decisiones técnicas
justificadas (y su alternativa descartada), y estrategia de tests. Todo debe
respetar la constitución y cubrir todos los RF. Marca qué RF cubre cada parte.
```

*Genera el [specs/001-tasks-mvp/plan.md](./specs/001-tasks-mvp/plan.md)*

---

## 5. Tareas

```text
A partir de spec.md y plan.md, genera specs/001-tasks-mvp/tasks.md:
tareas pequeñas (máx. 20-30 min cada una), en orden de dependencia, cada una
con los RF que cubre y una línea "Hecho cuando:" verificable. Usa checkboxes.
```

*Genera el [specs/001-tasks-mvp/tasks.md](./specs/001-tasks-mvp/tasks.md)*

---

## 6. Implementación

```text
Implementa SOLO la tarea T2 de specs/001-tasks-mvp/tasks.md, siguiendo
plan.md y la constitución. Escribe primero los tests, luego el código.
Ejecuta pytest -q y muéstrame el resultado. Al terminar: marca T2 en tasks.md,
indica qué RF cubre y PÁRATE. No empieces T3.
```

*Genera la implementación del código dentro de /tasks*

---

## 7. Validación

```text
Recorre specs/001-tasks-mvp/spec.md requisito por requisito (RF-1 a RF-11).
Para cada uno indica: qué test lo cubre, y el resultado de ejecutarlo.
Si algún RF no está cubierto o falla, dilo claramente. Después comprueba los
criterios de finalización y dame un veredicto: ¿la spec está cumplida?
```

---

## 8. Próximos pasos

```text
Nuevo requisito para tasks-cli: añadir una fecha límite a una tarea con
`tasks add <nombre> --due <fecha>`. NO toques código. Primero: actualiza
specs/001-tasks-mvp/spec.md (nuevo RF con EARS + casos límite: ¿y si la fecha 
es en el pasado? ¿cómo se muestra en la lista de pendientes?) y muéstrame el diff de la spec.
```