from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class Service(ABC):
    def __init__(self, db: AsyncSession):
        self.db = db
