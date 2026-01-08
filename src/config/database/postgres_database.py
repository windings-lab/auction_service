from sqlalchemy.engine import URL

from .base_database import BaseDatabase


class PostgresDatabase(BaseDatabase, engine="postgres"):
    def __init__(self):
        super().__init__()
        self.driver_name = "postgresql+asyncpg"
        if self.db_port is None:
            self.db_port = 5432

    def url(self) -> URL:
        url = URL.create(
            drivername=self.driver_name,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name
        )
        return url