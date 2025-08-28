from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import engine
import src.model
from src.auction.routers import router as auction_router
from src.account.routers import router as account_router
from src.etl.routers import router as etl_router


@asynccontextmanager
async def lifespan(in_app: FastAPI):
    yield
    # Shutdown code: nothing for now
    await engine.dispose()

fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(auction_router)
fastapi_app.include_router(account_router)
fastapi_app.include_router(etl_router)
