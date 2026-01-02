import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import engine
from src.auction.routers import router as auction_router
from src.account.routers import router as account_router

async def test_db_connection():
    try:
        async with engine.connect():
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"Failed to connect to the database: {str(e)}. API won't work correctly.")
        sys.exit(1)  # Exit with error code 1

@asynccontextmanager
async def lifespan(in_app: FastAPI):
    await test_db_connection()
    yield
    # Shutdown code: nothing for now
    await engine.dispose()

fastapi_app = FastAPI(lifespan=lifespan)
fastapi_app.include_router(auction_router)
fastapi_app.include_router(account_router)
