# IKAMONEY

Proyecto base: **React** (frontend) + **FastAPI** (backend) + **MySQL** (base de datos).
Por ahora solo contiene la "tubería": una pantalla que pide un mensaje al backend, y el backend lo lee de la base de datos.

## Qué necesitas instalado (antes de empezar)

| Herramienta | Versión | Cómo verificar |
|---|---|---|
| Git | cualquiera | `git --version` |
| Docker Desktop (abierto y corriendo) | reciente | `docker --version` |
| Python | 3.11 o superior | `python --version` (en Mac/Linux: `python3 --version`) |
| Node.js | 20 o superior | `node --version` |

MySQL **no** se instala: corre dentro de Docker.

## Arranque en 8 pasos

Abre **tres terminales** en la carpeta del repo. Los comandos son para Mac/Linux; las variantes de Windows (PowerShell) van marcadas.

**1. Clona el repo**
```bash
git clone <URL-DEL-REPO> ikamoney
cd ikamoney
```

**2. Crea tu archivo `.env`** (los valores de ejemplo sirven tal cual para desarrollo local)
```bash
cp .env.example .env
```
Windows: `copy .env.example .env`

**3. Levanta la base de datos** (terminal 1, desde la raíz)
```bash
docker compose up -d
docker compose ps
```
Espera a que la columna de estado diga `healthy` (puede tardar ~30 s la primera vez).

**4. Prepara el backend** (terminal 2)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Windows: `python -m venv .venv` y luego `.venv\Scripts\Activate.ps1`

**5. Arranca el backend** (misma terminal 2, con el entorno activado)
```bash
uvicorn app.main:app --reload --port 8000
```
Comprueba: abre http://localhost:8000/api/health → debe decir `{"status":"ok"}`.
Y http://localhost:8000/api/ping-db → debe mostrar el mensaje que viene de MySQL.

**6. Arranca el frontend** (terminal 3)
```bash
cd frontend
npm install
npm run dev
```

**7. Abre http://localhost:5173**
Debes ver ✅ y el mensaje *"La tubería funciona: este mensaje viene de MySQL."*

**8. Si ya terminaste de armar esto: pásaselo a otra persona**
Quien lo pruebe debe seguir este README desde cero, en una carpeta nueva, y llenar `docs/VALIDACION_COMPANERO.md`. Todo lo que se atore es un error del README: corrígelo.

## Estructura: dónde va cada cosa

```
ikamoney/
├── .env.example            # plantilla de variables (el .env real NO se sube)
├── docker-compose.yml      # solo la base de datos
├── db/init.sql             # tabla de prueba (se reemplaza con el modelo real en T18)
├── docs/                   # documentación y checklists
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py         # crea la app y registra los routers
│       ├── core/           # configuración y conexión a la BD
│       ├── api/routes/     # endpoints: un archivo por módulo (siempre bajo /api)
│       ├── models/         # tablas SQLAlchemy
│       ├── schemas/        # esquemas Pydantic de entrada/salida
│       └── services/       # lógica de negocio (las rutas llaman aquí)
└── frontend/
    └── src/
        ├── api/            # client.js: única puerta al backend
        ├── components/     # piezas reutilizables
        ├── pages/          # una pantalla por archivo
        └── hooks/          # hooks propios
```

`pages/PipelineCheck.jsx`, `api/routes/health.py` (`/ping-db`) y `db/init.sql` son **temporales**: se retiran cuando existan los módulos reales.

## Secretos: reglas

- Todo lo sensible va en `.env`, que está en `.gitignore`. **Nunca** en el código ni en `.env.example`.
- Los valores de `.env.example` son solo para desarrollo local y no sirven para nada fuera de tu máquina.
- Antes de cada commit: `git status` y revisa que `.env` no aparezca.
- **Si subes un secreto por error, avisa de inmediato al grupo.** Borrarlo en un commit nuevo no basta: queda en el historial y hay que rotar la llave.

## Si algo falla

| Síntoma | Qué revisar |
|---|---|
| `docker compose up` falla con "port is already allocated" | Ya tienes un MySQL local en el 3306. Cambia `MYSQL_PORT=3307` **y** el puerto en `DATABASE_URL` en tu `.env`, y repite el paso 3. |
| El backend dice `Access denied` o `Can't connect` | `DATABASE_URL` no coincide con las variables `MYSQL_*` del `.env`, o la BD aún no está `healthy`. |
| Cambiaste usuario/contraseña de MySQL y sigue sin entrar | MySQL solo lee esas variables la primera vez. Reinicia desde cero: `docker compose down -v` y luego `docker compose up -d` (borra los datos locales). |
| `/api/ping-db` da 503 o "table doesn't exist" | La BD se creó sin `init.sql`. Mismo remedio: `docker compose down -v && docker compose up -d`. |
| Pantalla con ❌ en el navegador | Backend apagado, o `CORS_ORIGINS` no incluye la URL desde la que abres el frontend. |
| `pydantic ValidationError: database_url` | No existe `.env` en la **raíz** del repo (paso 2). |
| `python` o `pip` no encontrados (Windows) | Prueba `py -m venv .venv` y reinstala Python marcando "Add to PATH". |

Si llevas más de media jornada atorado con la conexión a la base de datos, dilo en el grupo.

## Despliegue (referencia)

- Frontend: Vercel, con carpeta raíz `frontend` y la variable `VITE_API_URL` apuntando a la URL pública del backend.
- Backend y base de datos en producción: por definir.
