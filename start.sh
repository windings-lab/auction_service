#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."

until pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up - starting application"

# Run your application command
uv run alembic upgrade head
uv run uvicorn app.main:fastapi_app --host "0.0.0.0" --port "8080"