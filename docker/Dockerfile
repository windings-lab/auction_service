FROM python:3.13-alpine

ARG DB_ENGINE
RUN if [ "$DB_ENGINE" = "postgres" ]; then \
        apk add --no-cache postgresql-client; \
    elif [ "$DB_ENGINE" = "mysql" ]; then \
        apk add --no-cache mariadb-client mariadb-connector-c-dev; \
    fi

WORKDIR /app

COPY ../pyproject.toml ../uv.lock ./

RUN pip install --no-cache-dir uv && uv sync --no-dev --group "$DB_ENGINE"

COPY ../alembic.ini ../config.ini ../start.sh ./
COPY ../src/ ./src

RUN chmod +x start.sh

CMD ["sh", "./start.sh"]
