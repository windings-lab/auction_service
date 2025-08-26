#!/bin/sh
set -e

echo "Waiting for database..."

if [ "$DB_ENGINE" = "postgres" ]; then
  until pg_isready -h "$DB_HOST" -p "${DB_PORT:-5432}" -U "$DB_USER"; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
  done
  echo "PostgreSQL is up"
elif [ "$DB_ENGINE" = "mysql" ]; then
  until mysqladmin ping -h "$DB_HOST" -P"${DB_PORT:-3306}" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
    echo "MySQL is unavailable - sleeping"
    sleep 2
  done
  echo "MySQL is up"
else
  echo "Unsupported DB_ENGINE: $DB_ENGINE"
  exit 1
fi

echo "Starting application"

uv run --no-dev alembic upgrade head
uv run --no-dev uvicorn app.main:fastapi_app --host "0.0.0.0" --port "8080"