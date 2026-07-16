.PHONY: up down build logs shell test lint format init-db seed reset-db

## Start db + app (build if needed)
up:
	docker compose up -d --build

## Stop and remove containers (keeps the data volume)
down:
	docker compose down

## Rebuild the app image from scratch
build:
	docker compose build --no-cache

## Follow logs from both services
logs:
	docker compose logs -f

## Open a shell inside the running app container
shell:
	docker compose exec app bash

## Run the test suite
test:
	docker compose exec app pytest -q

## Lint the codebase
lint:
	docker compose exec app ruff check .

## Auto-format the codebase
format:
	docker compose exec app ruff format .

## Create tables from the current SQLAlchemy models + mark Alembic as up to date
## (use this once, on a fresh/empty database)
init-db:
	docker compose exec app python -m app.db.init_db
	docker compose exec app alembic stamp head

## Load sample data from seed_data/ (safe to re-run)
seed:
	docker compose exec app psql -f seed_data/seed_booking_api.sql
	docker compose exec app psql -f seed_data/seed_booking_workload.sql

## Wipe the database volume and rebuild schema + sample data from scratch
reset-db:
	docker compose down -v
	docker compose up -d --build
	$(MAKE) init-db
	$(MAKE) seed
