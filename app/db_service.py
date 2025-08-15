from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class DBService(ABC):
    def __init__(self, db: AsyncSession):
        self.db = db
