#!/bin/sh
set -e

uv run alembic upgrade head
uv run uvicorn src.main:fastapi_app --host "0.0.0.0" --port "8080"