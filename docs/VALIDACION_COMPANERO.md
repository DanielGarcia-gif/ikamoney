# Validación con un compañero (paso 8 de la tarea)

La tarea NO está terminada hasta que otra persona lo logre sin ayuda tuya.

- [ ] Nombre de quien probó: __________  Sistema operativo: __________
- [ ] Clonó el repo en una carpeta nueva (no la tuya, y fuera de OneDrive)
- [ ] Siguió el README sin preguntarte nada
- [ ] `docker compose ps` muestra la base de datos `healthy`
- [ ] `alembic upgrade head` terminó sin errores
- [ ] `alembic current` dice `0001 (head)`
- [ ] `SHOW TABLES` muestra 12 tablas (11 del modelo + `alembic_version`)
- [ ] http://localhost:8000/api/health responde `{"status":"ok"}`
- [ ] http://localhost:5173 muestra ✅ y "Esquema en la migración 0001"
- [ ] Prueba de reinicio: `docker compose down -v`, `docker compose up -d` y `alembic upgrade head` dejan todo igual
- [ ] Tiempo total: ______ min (meta: menos de 15)
- [ ] Pasos del README que confundieron o faltaron (corregirlos antes de cerrar):
  -
