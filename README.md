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

## Initialize the database

Migrations define the schema; the SQL files under `seed_data/` provide sample rows for manual verification.

```bash
# 1. Apply migrations (creates all tables)
docker compose exec app alembic upgrade head

# 2. Load sample data (safe to re-run)
docker compose exec -T db psql -U postgres -d booking_api < seed_data/seed_booking_api.sql
docker compose exec -T db psql -U postgres -d booking_api < seed_data/seed_booking_workload.sql
```

If you're working inside the Dev Container's integrated terminal instead, drop `docker compose exec app` and just run `alembic upgrade head` directly (you're already inside the `app` container).

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

## Known limitations

- Dev-only setup: the Dockerfile is not multi-stage / production-hardened (no non-root user, no slim runtime-only image).
- No automatic migration-on-startup — `alembic upgrade head` is a manual step, to keep DB state changes explicit during development.
- Seed scripts are plain SQL run manually; no CLI wrapper.
- Postgres data persists in a named Docker volume (`booking_api_pgdata`) across restarts; delete it (`docker compose down -v`) if you want a clean slate.
