# Shipping Booking API

FastAPI service for booking detail lookup (Practice 1) and office booking-workload summaries (Practice 2), containerized for local development with Docker / Dev Container (Practice 3).

## Stack

- FastAPI + SQLAlchemy + Alembic
- PostgreSQL 16
- Dependency management: [uv](https://docs.astral.sh/uv/)
- Dev environment: Docker Compose + VS Code Dev Container

## Project layout

```
app/
  routers/     # HTTP layer (FastAPI routers)
  services/     # business logic
  repositories/  # SQL / DB access
  schemas/      # Pydantic request/response models
  models/       # SQLAlchemy ORM models
alembic/        # DB migrations
seed_data/      # sample data for local verification
tests/          # unit tests (services layer, repositories mocked)
```

## Option A — Run with Dev Container (recommended)

Requires Docker Desktop + VS Code with the "Dev Containers" extension.

1. Copy the env example: `cp .env.example .env` (defaults work out of the box, no editing required).
2. Open the project folder in VS Code.
3. Command Palette → **Dev Containers: Reopen in Container**.
   - This builds the `app` service from `.devcontainer/Dockerfile`, starts the `db` (Postgres) service, waits for its healthcheck, then runs `uv sync --frozen` inside the container (`postCreateCommand`).
4. Once the container is ready, open a terminal **inside VS Code** (it runs inside the `app` container) and continue with the steps in "Initialize the database" below.

## Option B — Run with plain Docker Compose (no VS Code)

```bash
cp .env.example .env
docker compose up -d --build
```

This starts both `db` and `app`. The API will be reachable at `http://localhost:8000` once the database is initialized (next section).

## Makefile shortcuts (run from the host terminal, not inside the Dev Container)

A `Makefile` wraps the commands below into short targets — useful once you're past the first manual walkthrough:

```bash
make up         # docker compose up -d --build
make init-db    # create tables + alembic stamp head (fresh DB only)
make seed       # load both seed_data/*.sql files
make test       # run pytest inside the app container
make lint       # ruff check .
make format     # ruff format .
make reset-db   # wipe the volume and rebuild schema + sample data from scratch
make shell      # open a bash shell inside the app container
make down       # stop containers (keeps the data volume)
```

Run `make` from the host (Ubuntu/WSL terminal), not from the Dev Container's integrated terminal — these targets call `docker compose`, which needs access to the Docker CLI that the `app` container itself doesn't have.

## Initialize the database

**On a brand-new database** (fresh volume, e.g. first time in the Dev Container), `alembic upgrade head` alone is *not* enough: the first migration (`6430a5cd51fb_baseline_existing_schema`) is an intentional no-op that assumes the schema already exists. Create the tables from the SQLAlchemy models first, then have Alembic mark itself as up to date:

```bash
python -m app.db.init_db   # creates all tables from the current models
alembic stamp head          # tells Alembic the schema is already at the latest revision
```

Then load the sample rows:

```bash
psql -f seed_data/seed_booking_api.sql
psql -f seed_data/seed_booking_workload.sql
```

(`psql` is pre-configured via `PGHOST`/`PGUSER`/`PGPASSWORD`/`PGDATABASE` to reach `db` without prompting for a password — run these from inside the Dev Container's integrated terminal, or prefix each with `docker compose exec app` if you're on the host machine instead of VS Code.)

**On a database that was already schema-migrated by a previous run** (e.g. you're only adding a new column later), use the normal `alembic upgrade head` instead — `init_db.py` + `stamp head` is only for bootstrapping an empty database.

## Run the application

Already running via `docker compose up` / Dev Container (`uvicorn --reload`, hot reload on code changes thanks to the bind-mounted source).

To run it manually inside the container:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify:

```bash
curl http://localhost:8000/api/v1/bookings/BKG0000001
curl "http://localhost:8000/api/v1/offices/RICHQ/booking-workload-summary?minutes=3000"
```

Interactive docs: `http://localhost:8000/docs`

## Run tests

```bash
docker compose exec app pytest
```

(or `pytest` directly inside the Dev Container terminal). Tests mock the repository layer, so **no database connection is required** to run them.

## Environment variables

| Variable | Purpose | Example |
|---|---|---|
| `POSTGRES_DB` | Database name created by the `db` container | `booking_api` |
| `POSTGRES_USER` | Postgres user | `postgres` |
| `POSTGRES_PASSWORD` | Postgres password | `123456` |
| `DATABASE_URL` | SQLAlchemy connection string used by the app | see `.env.example` |

See `.env.example` for the full example file. `.env` is git-ignored — never commit real credentials.

Note: `DATABASE_URL` in `.env` points at `localhost:5498` for running the app *outside* Docker. When the `app` service runs via Docker Compose, `docker-compose.yaml` overrides `DATABASE_URL` to use the `db` hostname (`db:5432`) instead, since `localhost` inside a container refers to the container itself, not the `db` service.

## Troubleshooting

**`error during connect: ... dockerDesktopLinuxEngine ... The system cannot find the file specified` (Windows)**
Docker Desktop isn't running. Start it and wait until the whale icon in the system tray stops animating before retrying.

**`failed to connect to the docker API at unix:///var/run/docker.sock` (WSL/Ubuntu)**
Docker Desktop's WSL integration isn't enabled for your distro. Docker Desktop → Settings → Resources → WSL Integration → enable your Ubuntu distro → Apply & Restart. Verify with `docker ps` from inside the WSL terminal (not PowerShell).

**`Error response from daemon: Conflict. The container name "/booking-api-db" is already in use`**
A container from a previous attempt (a partial build, a manual `docker compose up`, etc.) is still around under the same name. Remove it: `docker rm -f booking-api-db booking-api-app`, then retry.

**`psql: error: ... fe_sendauth: no password supplied`**
You're running `psql` without the `PG*` environment variables — this only happens if you're *outside* the `app` container (e.g. trying `psql` directly on the host, or in a shell that didn't inherit the container's environment). Run `psql` from inside the `app` container, or `docker compose exec app psql ...` from the host.

**`sqlalchemy.exc.ProgrammingError: relation "bookings" does not exist` when running `alembic upgrade head`**
Expected on a brand-new/empty database — see "Initialize the database" above. The first migration is a no-op baseline; use `python -m app.db.init_db` + `alembic stamp head` instead of `alembic upgrade head` for a fresh database.

**API returns `{"detail": "Internal server error"}` but `GET /` works**
`GET /` doesn't touch the database, so it succeeding just proves the app process is up. A 500 on the real endpoints almost always means the schema/tables aren't there yet — run the "Initialize the database" steps.

**Dev Containers extension log ends with just `Exit code 1` and no visible error**
The VS Code terminal panel truncates long build logs. Re-run the equivalent command directly in your host terminal — `docker compose up -d --build` — to see the full, unclipped error output.

## Known limitations

- Dev-only setup: the Dockerfile is not multi-stage / production-hardened (no non-root user, no slim runtime-only image).
- No automatic migration-on-startup — `alembic upgrade head` is a manual step, to keep DB state changes explicit during development.
- The oldest migration (`6430a5cd51fb`) is a no-op baseline written for a database that was schema-migrated outside Alembic — bootstrapping a fresh database needs `python -m app.db.init_db` + `alembic stamp head` instead of a plain `alembic upgrade head` (see "Initialize the database" above). A cleaner fix would be regenerating that migration with real `CREATE TABLE` statements.
- Seed scripts are plain SQL, wrapped by `make seed` — no upsert/idempotency logic beyond what each `.sql` file does itself.
- Postgres data persists in a named Docker volume (`booking_api_pgdata`) across restarts; `make reset-db` (or `docker compose down -v`) wipes it for a clean slate.
- `ruff` is wired up (`make lint` / `make format`) but the existing Practice 1/2 code hasn't been run through it yet — expect some pre-existing lint findings (unused imports, a few long lines) until someone does a dedicated cleanup pass.
