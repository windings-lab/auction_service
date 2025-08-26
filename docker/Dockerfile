FROM python:3.13-alpine

RUN apk add --no-cache postgresql-client

WORKDIR /app

COPY ../pyproject.toml ../uv.lock ./

RUN pip install --no-cache-dir uv && uv sync --no-dev

COPY ../alembic.ini ../start.sh ./
COPY ../app ./app

RUN chmod +x start.sh

CMD ["sh", "./start.sh"]
