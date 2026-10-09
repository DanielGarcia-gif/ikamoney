# IKAMONEY

Proyecto base: **React** (frontend) + **FastAPI** (backend) + **MySQL** (base de datos).
La base de datos se crea y se actualiza con **migraciones** (Alembic): nadie crea tablas a mano.

## Qué necesitas instalado

| Herramienta | Versión | Cómo verificar |
|---|---|---|
| Git | cualquiera | `git --version` |
| Docker Desktop (abierto y corriendo) | reciente | `docker --version` |
| Python | 3.11 o superior | `python --version` (Mac/Linux: `python3 --version`) |
| Node.js | 20 o superior | `node --version` |

MySQL **no** se instala: corre dentro de Docker. (¿No puedes usar Docker? Ve a [Sin Docker](#sin-docker).)

> **No trabajes dentro de OneDrive** ni de otra carpeta sincronizada. `node_modules` y `.venv` tienen miles de archivos y la sincronización los vuelve lentos o los bloquea. Usa algo como `C:\proyectos\ikamoney` o `~/proyectos/ikamoney`.

## Arranque en 8 pasos

Necesitas **tres terminales** abiertas en la carpeta del repo.

**1. Clona el repo**
```bash
git clone <URL-DEL-REPO> ikamoney
cd ikamoney
```

**2. Crea tu archivo `.env`** (los valores de ejemplo sirven tal cual en local)

| Mac / Linux | Windows (PowerShell) |
|---|---|
| `cp .env.example .env` | `copy .env.example .env` |

**3. Levanta la base de datos** (terminal 1, raíz del repo)
```bash
docker compose up -d
docker compose ps
```
Espera a que el estado diga `healthy` (~30 s la primera vez). La base queda **vacía**: las tablas las crea el paso 5.

**4. Prepara el backend** (terminal 2)

Mac / Linux:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Windows (PowerShell):
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Si PowerShell dice que la ejecución de scripts está deshabilitada, corre una vez `Set-ExecutionPolicy -Scope Process RemoteSigned` y repite la activación. Verás `(.venv)` al inicio de la línea cuando esté activo.

**5. Crea las tablas y arranca el backend** (misma terminal, con `(.venv)` activo y dentro de `backend/`)
```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
`alembic upgrade head` debe terminar sin errores y mostrar una línea `Running upgrade  -> 0001`.
Comprueba en el navegador:
- http://localhost:8000/api/health → `{"status":"ok"}`
- http://localhost:8000/api/ping-db → `{"message":"Base de datos conectada. Esquema en la migración 0001."}`

**6. Arranca el frontend** (terminal 3)
```bash
cd frontend
npm install
npm run dev
```

**7. Abre http://localhost:5173**
Debes ver ✅ y el mensaje *"Base de datos conectada. Esquema en la migración 0001."*

**8. Pásaselo a otra persona**
Quien lo pruebe debe seguir este README desde cero, en una carpeta nueva, y llenar `docs/VALIDACION_COMPANERO.md`. Todo lo que se atore es un error del README: corrígelo.

## Base de datos y migraciones

El modelo de datos (T18) vive en `backend/app/models/` (un archivo por tabla). Los cambios al esquema viajan en **migraciones**: archivos en `backend/alembic/versions/` que Alembic aplica en orden. Así todos tienen exactamente las mismas tablas.

Todos los comandos de `alembic` se corren **dentro de `backend/`** y con `(.venv)` activo.

### Crear la base desde cero
```bash
docker compose up -d          # raíz del repo
cd backend
alembic upgrade head          # crea las 11 tablas (+ alembic_version)
```
Para empezar de cero (borra todos los datos locales): desde la raíz `docker compose down -v`, luego `docker compose up -d` y de nuevo `alembic upgrade head`.

### Comprobar que quedó bien
```bash
alembic current               # debe decir: 0001 (head)
docker compose exec db mysql -u ikamoney -pikamoney_local_cambiar ikamoney -e "SHOW TABLES;"
```
Deben aparecer 12 tablas: las 11 del modelo más `alembic_version`. (Si cambiaste usuario o contraseña en `.env`, usa los tuyos. Si cambiaste el puerto, no afecta este comando.)

### Cada vez que hagas `git pull`
Si llegaron migraciones nuevas, aplícalas antes de seguir trabajando:
```bash
alembic upgrade head
```

### Cambiar el esquema (agregar una tabla o columna)
1. Edita o crea el modelo en `backend/app/models/`. Si es un archivo nuevo, importa su clase en `app/models/__init__.py` (si no, Alembic no lo ve).
2. Genera la migración: `alembic revision --autogenerate -m "describe el cambio"`
3. **Abre el archivo generado y revísalo.** Alembic se equivoca a veces (por ejemplo, no detecta los `CHECK` ni los cambios de valores de un `ENUM`; esos se agregan a mano).
4. Aplícala: `alembic upgrade head`
5. Sube **modelo y migración en el mismo commit**.

### Reglas del equipo
- **Nunca edites una migración que ya está en el repo.** Si te equivocaste, crea otra migración que lo corrija.
- **Nunca cambies tablas a mano** (con un cliente SQL): tu base dejaría de coincidir con la de los demás.
- Para deshacer la última migración en tu máquina: `alembic downgrade -1`.
- Si dos personas crean una migración al mismo tiempo, Alembic avisa `Multiple head revisions`. Avisa en el grupo: se resuelve con `alembic merge -m "unir ramas" <rev1> <rev2>`.

### `db/schema.sql`
Es una copia de **solo lectura** del esquema inicial en SQL, para revisarlo sin abrir Python. **No se ejecuta**: la fuente de verdad son las migraciones.

## Estructura: dónde va cada cosa

```
ikamoney/
├── .env.example            # plantilla de variables (el .env real NO se sube)
├── docker-compose.yml      # solo la base de datos
├── db/schema.sql           # referencia del esquema (solo lectura)
├── docs/                   # documentación y checklists
├── backend/
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py          # conecta Alembic con la app y la base
│   │   └── versions/       # una migración por cambio, en orden
│   └── app/
│       ├── main.py         # crea la app y registra los routers
│       ├── core/           # configuración y conexión a la BD
│       ├── api/routes/     # endpoints: un archivo por módulo (siempre bajo /api)
│       ├── models/         # tablas SQLAlchemy: un archivo por tabla
│       ├── schemas/        # esquemas Pydantic de entrada/salida
│       └── services/       # lógica de negocio (las rutas llaman aquí)
└── frontend/
    └── src/
        ├── api/            # client.js: única puerta al backend
        ├── components/     # piezas reutilizables
        ├── pages/          # una pantalla por archivo
        └── hooks/          # hooks propios
```

`frontend/src/pages/PipelineCheck.jsx` y `/api/ping-db` son **temporales**: se retiran cuando existan las pantallas y módulos reales.

## Secretos: reglas

- Todo lo sensible va en `.env`, que está en `.gitignore`. **Nunca** en el código ni en `.env.example`.
- Los valores de `.env.example` son solo para desarrollo local.
- Antes de cada commit: `git status` y revisa que `.env` no aparezca.
- **Si subes un secreto por error, avisa de inmediato al grupo.** Borrarlo en un commit nuevo no basta: queda en el historial y hay que rotar la llave.

## Si algo falla

| Síntoma | Qué revisar |
|---|---|
| Docker Desktop: "Virtualization support not detected" o `wsl --install` da "Error catastrófico" | La virtualización está apagada en la BIOS (VT-x en Intel, SVM Mode en AMD). Actívala, reinicia y corre `wsl --install --web-download`. Si es una máquina virtual o la BIOS está bloqueada, usa [Sin Docker](#sin-docker). |
| Docker Desktop se queda en "Engine starting" | Espera hasta 5 minutos la primera vez. Si sigue: cierra Docker, corre `wsl --shutdown` y ábrelo de nuevo. |
| `docker compose up` falla con "ports are not available" / "port is already allocated" | Ya tienes un MySQL local en el 3306. En tu `.env` cambia `MYSQL_PORT=3307` **y** el puerto dentro de `DATABASE_URL` (`...@localhost:3307/ikamoney`). Luego `docker compose down -v` y `docker compose up -d`. |
| `pydantic ValidationError: database_url` | No existe `.env` en la **raíz** del repo (paso 2). |
| `alembic: command not found` / "no se reconoce" | No tienes `(.venv)` activo o no estás dentro de `backend/`. Repite el paso 4. |
| `alembic upgrade head` da `Can't connect` / `Access denied` | La base aún no está `healthy`, o `DATABASE_URL` no coincide con las variables `MYSQL_*` del `.env` (usuario, contraseña y puerto). |
| `alembic upgrade head` da `Table ... already exists` | Tu base tiene tablas de antes. Empieza de cero: raíz del repo, `docker compose down -v`, `docker compose up -d`, y repite `alembic upgrade head`. |
| `/api/ping-db` da 503 "¿Corriste las migraciones?" | Falta `alembic upgrade head` (paso 5). |
| Cambiaste usuario/contraseña de MySQL y sigue sin entrar | MySQL solo lee esas variables la primera vez. `docker compose down -v` y `docker compose up -d` (borra los datos locales). |
| Pantalla con ❌ en el navegador | Backend apagado, o `CORS_ORIGINS` no incluye la URL desde la que abres el frontend. El mensaje entre paréntesis dice el motivo. |
| `python` o `pip` no se reconocen (Windows) | Prueba `py -m venv .venv` y reinstala Python marcando "Add to PATH". |
| `npm install` o `pip install` muy lentos o con "archivo bloqueado" | Estás dentro de OneDrive. Mueve el proyecto a `C:\proyectos\ikamoney`. |

Si llevas más de media jornada atorado con la conexión a la base de datos, dilo en el grupo.

## Sin Docker

Solo si no puedes usar Docker. Pierdes la garantía de que todos tengan la misma versión de MySQL, así que usa **MySQL 8.0 o superior** (no MariaDB).

1. Instala MySQL 8 (Mac: `brew install mysql@8.0`; Windows: `winget install Oracle.MySQL` o el instalador oficial; Linux: `sudo apt install mysql-server`).
2. Entra como administrador (`mysql -u root -p`) y crea la base y el usuario:
   ```sql
   CREATE DATABASE ikamoney CHARACTER SET utf8mb4;
   CREATE USER 'ikamoney'@'localhost' IDENTIFIED BY 'ikamoney_local_cambiar';
   GRANT ALL PRIVILEGES ON ikamoney.* TO 'ikamoney'@'localhost';
   ```
3. En tu `.env`, deja `DATABASE_URL` con tu usuario, contraseña y puerto reales.
4. Salta el paso 3 del arranque y sigue desde el 4. Las tablas las crea igual `alembic upgrade head`.

## Despliegue (referencia)

- Frontend: Vercel, con carpeta raíz `frontend` y la variable `VITE_API_URL` apuntando a la URL pública del backend.
- Backend y base de datos en producción: por definir. En cualquier ambiente, el esquema se aplica con `alembic upgrade head`.
