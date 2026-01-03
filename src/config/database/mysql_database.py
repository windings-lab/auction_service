from sqlalchemy.engine import URL

from .base_database import BaseDatabase


class MySQLDatabase(BaseDatabase, engine="mysql"):
    def __init__(self, config):
        super().__init__(config)
        self.driver_name = "mysql+aiomysql"
        if self.db_port is None:
            self.db_port = 3306

    def url(self) -> URL:
        query = {
            "charset": "utf8mb4",
        }

        url = URL.create(
            drivername=self.driver_name,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query=query,
        )
        return url