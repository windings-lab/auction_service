from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from .config import settings

engine = create_async_engine(
    settings.db_url,
    future=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session() as session:
        yield session