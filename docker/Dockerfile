FROM python:3.13-alpine

RUN apk add --no-cache postgresql-client mariadb-client

WORKDIR /app

COPY ../pyproject.toml ../uv.lock ./

RUN pip install --no-cache-dir uv

COPY ../alembic.ini ../config.ini ../start.sh ./
COPY ../src/ ./src

RUN chmod +x start.sh

CMD ["sh", "./start.sh"]
