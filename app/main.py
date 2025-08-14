from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import engine, Base
import models # import all models to register them
import auction


@asynccontextmanager
async def lifespan(in_app: FastAPI):
    # Startup code: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown code: nothing for now

fastapi = FastAPI(lifespan=lifespan)
fastapi.include_router(auction.router)
