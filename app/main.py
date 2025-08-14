from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import engine
from .models import Base


@asynccontextmanager
async def lifespan(in_app: FastAPI):
    # Startup code: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown code: nothing for now

app = FastAPI(lifespan=lifespan)
