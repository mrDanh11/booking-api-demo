FROM python:3.11-slim

# System deps: psycopg needs libpq at runtime, gcc only if a wheel is missing.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv is the package manager this project already uses (pyproject.toml + uv.lock)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

ENV UV_PROJECT_ENVIRONMENT=/usr/local \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

# Copy dependency manifests first so dependency install is cached
# separately from application code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# App code is bind-mounted by docker-compose/devcontainer at runtime,
# so we don't COPY it here for the dev image.

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
