from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings

db_engine = create_async_engine(
    settings.database.url(),
    future=True
)

async_session = async_sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
    autoflush=False
)


async def db_connect():
    try:
        async with db_engine.connect():
            print("Successfully connected to the database!")
    except Exception as e:
        raise Exception(f"Failed to connect to the database: {str(e)}. API won't work correctly.")


async def get_session(self) -> AsyncGenerator[AsyncSession | Any, Any]:
    async with self.async_session() as session:
        yield session