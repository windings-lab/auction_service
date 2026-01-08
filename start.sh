#!/bin/sh
set -e

uv run alembic upgrade head
uv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:fastapi_app -b 0.0.0.0:8080