# Auction Service

A project for managing online auctions with support for bids and lot statuses.

## Features

### Completed
- [x] Project initialization
- [x] Creation of database connections for PostgreSQL and SQLite
- [x] Initialization of Alembic and migrations
- [x] Creation of Docker configuration
- [x] Creation of auction database models (Lot, Bid)
- [x] Creation of auction endpoints using Pydantic serialization
  - [x] `POST /lots` — create a lot
  - [x] `POST /lots/{lot_id}/bids` — place a bid for a user. Not allowed if the lot status is inactive. Broadcasting websocket
  - [x] `PATCH /lots/{lot_id}/bids` — update bid amount for the use. Not allowed if the lot status is inactive. Broadcasting websocket
  - [x] `GET /lots` — list of active lots
  - [x] `PATCH /{lot_id}/status` — update lot status. Broadcasting websocket
- [x] Structuring of base code (separate folders for models, services, and endpoints)
- [x] User account creation with JWT-based authentication
- [x] Creation and update of bids based on the authenticated user
- [x] WebSocket for real-time lot status updates
  - [x] `WEBSOCKET /ws/lots/{lot_id}` - endpoint for subscribing to events
- [x] WebSocket python cli client

### Optional
- [ ] Writing tests using pytest
- [ ] Sending WebSocket messages to a Telegram bot
- [ ] Configuring secure environment variables, e.g., password
- [ ] Using Redis or RabbitMQ as a broker for Websocket
- [ ] Using Redis for storing user sessions
- [ ] Using Celery to execute Websocket Tasks
- [ ] Websocket server refactored to be easier to scale. Separate FastAPI code and WebSocket code

## Running the application (prod)

1. Make sure uv installed in your system or use pip venv for installing uv 

db_engine = mssql | postgres | mysql

```bash
uv init # if uv installed system-wide
uv venv # if uv installed system-wide
uv sync --no-dev --group <db_engine>
uv run alembic upgrade head
uv run uvicorn src.main:fastapi_app
```

#### MSSQL

1. Use ODBC Driver 18 for SQL Server
2. Manually create a necessary database or use your database
3. Create the necessary user or use your user
4. Edit config.ini if needed

## Running the application (Dev)

1. Make sure uv installed in your system or use pip venv for installing uv 

```bash
uv init # if uv installed system-wide
uv venv # if uv installed system-wide
uv sync
uv run alembic upgrade head
uv run uvicorn src.main:fastapi_app
```

## Running the application (Docker)

1. Make sure Docker Engine is running
2. In the project root folder, run:

PostgreSQL
```bash
docker compose -f docker/docker-compose.yaml -f docker/docker-compose.override-postgres.yml up
```

MySQL
```bash
docker compose -f docker/docker-compose.yaml -f docker/docker-compose.override-mysql.yml up
```

## Using ETL service

1. Make sure app is running
2. Open `<ip-address>:<port>/etl/`
3. Input your data and make excel table in csv format
4. Make sure that the first column in Excel is the column that you want to filter and extract

## Running the WebSocket client

```console
usage: websocket_client.py [-h] [--url URL] [--port PORT] lot_id

WebSocket client for lot updates

positional arguments:
  lot_id       ID of the lot to subscribe to

options:
  -h, --help   show this help message and exit
  --url URL    url to connect to
  --port PORT  port to connect to
```

## Environment variables

| Variable                      | Description                                                                              | Values    | Default                |
|-------------------------------|------------------------------------------------------------------------------------------|-----------|------------------------|
| `APP_SETTINGS`                | dev with SQLite or prod with PostgreSQL settings                                         | dev, prod | dev                    |
| `DB_ENGINE`                   | Database engine to use                                                                   |           | Error if not specified |
| `DB_NAME`                     | Database name                                                                            |           | db                     |
| `DB_HOST`                     | Database host                                                                            |           | localhost              |
| `DB_PORT`                     | Database port                                                                            |           | Based on Engine        |
| `DB_USER`                     | Database user                                                                            |           | Error if not specified |
| `DB_PASSWORD`                 | Database password                                                                        |           | Error if not specified |
| `MSSQL_DRIVER`                | Microsoft SQL Driver to use. For now only compatible with ODBC Driver 18 for SQL Server  |           | Error if not specified |
| `JWT_SECRET_KEY`              | Encoder key for JWT, use openssl rand -hex 32                                            |           | Error if not specified |
| `JWT_ALGORITHM`               | Encoder alghorithm type for JWT                                                          |           | HS256                  |
| `TOKEN_EXPIRATION_IN_MINUTES` | Expiration time for token                                                                |           | 30                     |
