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

## Running the application (Dev)

1. Create a uv Python interpreter
2. Make sure the required environment variables are set
3. In the project root folder, run:

```bash
uv sync
uv run uvicorn app.main:fastapi_app
```

## Running the application (Docker)

1. Make sure Docker Engine is running
2. In the project root folder, run:

```bash
docker-compose up -d
```

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

| Variable                      | Description                                      | Values    | Default   |
|-------------------------------|--------------------------------------------------|-----------|-----------|
| `APP_SETTINGS`                | dev with SQLite or prod with PostgreSQL settings | dev, prod | dev       |
| `PGHOST`                      | PostgreSQL host                                  |           | localhost |
| `PGPORT`                      | PostgreSQL port                                  |           | 5432      |
| `PGUSER`                      | PostgreSQL user                                  |           |           |
| `PGPASSWORD`                  | PostgreSQL password                              |           |           |
| `JWT_SECRET_KEY`              | Encoder key for JWT, use openssl rand -hex 32    |           |           |
| `JWT_ALGORITHM`               | Encoder alghorithm type for JWT                  |           | HS256     |
| `TOKEN_EXPIRATION_IN_MINUTES` | Expiration time for token                        |           | 30        |
