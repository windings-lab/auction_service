from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .db import engine
import app.model
from app.auction.routers import router as auction_router
from app.account.routers import router as account_router
from app.auction.lot_websocket_manager import manager


@asynccontextmanager
async def lifespan(in_app: FastAPI):
    # Startup code: create tables
    async with engine.begin() as conn:
        await conn.run_sync(app.model.Base.metadata.create_all)
    yield
    # Shutdown code: nothing for now

fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(auction_router)
fastapi_app.include_router(account_router)

@fastapi_app.websocket("/ws/lots/{lot_id}")
async def lot_websocket_endpoint(websocket: WebSocket, lot_id: int):
    await manager.connect(lot_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(lot_id, websocket)
