import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auction.routers import router as auction_router
from src.account.routers import router as account_router
from src.core.db import db_connect, db_engine

@asynccontextmanager
async def lifespan(in_app: FastAPI):
    await db_connect()
    yield
    # Shutdown code: nothing for now
    await db_engine.dispose()

fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(auction_router)
fastapi_app.include_router(account_router)
