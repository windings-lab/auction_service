from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import engine
import app.model
from app.auction.routers import router as auction_router


@asynccontextmanager
async def lifespan(in_app: FastAPI):
    # Startup code: create tables
    async with engine.begin() as conn:
        await conn.run_sync(app.model.Base.metadata.create_all)
    yield
    # Shutdown code: nothing for now

fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(auction_router)
