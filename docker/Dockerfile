FROM python:3.14.2-trixie
COPY --from=ghcr.io/astral-sh/uv:0.9.21 /uv /uvx /bin/

ARG DB_ENGINE=postgres

WORKDIR /app

ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED="True"

ENV UV_NO_CACHE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_DEV=0
ENV UV_FROZEN=1

RUN uv venv

ENV UV_PROJECT_ENVIRONMENT=/app/.venv
COPY ../pyproject.toml ../uv.lock ./

RUN uv sync --group "$DB_ENGINE"

COPY ../alembic.ini ../start.sh ./
COPY ../src/ ./src

RUN chmod +x start.sh

CMD ["./start.sh"]
