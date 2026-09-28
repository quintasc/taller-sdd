# Constitución del Proyecto
1. **Stack:** Python 3.10+ y stdlib; sin dependencias externas.
2. **Specs:** Implementación fiel; ante duda se para y pregunta, nunca se inventa.
3. **Roles:** `core.py` lógica pura (sin I/O ni disco). CLI única interfaz (solo parsea y formatea).
4. **Tests:** Siempre verdes (`pytest -q`); mínimo un test por regla de negocio.
5. **Persistencia:** JSON plano (esquema en el plan); sin DB, red ni formatos binarios.
6. **Idioma:** Código y docstrings en inglés; mensajes de interfaz en español.
