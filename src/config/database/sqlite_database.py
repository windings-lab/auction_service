from sqlalchemy.engine import URL

from .base_database import BaseDatabase


class SQLiteDatabase(BaseDatabase, engine="sqlite"):
    def __init__(self, config):
        super().__init__(config)
        self.driver_name = "sqlite+aiosqlite"
        self.db_name = "dev.db"

    def url(self) -> URL:
        url = URL.create(
            drivername=self.driver_name,
            database=self.db_name
        )
        return url