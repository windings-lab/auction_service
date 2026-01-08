import os

from sqlalchemy.engine import URL

from .base_database import BaseDatabase


class MSSQLDatabase(BaseDatabase, engine="mssql"):
    def __init__(self):
        super().__init__()
        self.driver_name = "mssql+aioodbc"
        self.mssql_driver = os.getenv("MSSQL_DRIVER", None)
        if not self.mssql_driver:
            raise EnvironmentError("MSSQL_DRIVER variable is not set")
        if not self.db_port:
            self.db_port = 1433

    def url(self) -> URL:
        query = {
            "driver": self.mssql_driver,
            "Trusted_Connection": "no",
            "TrustServerCertificate": "yes",
            "UID": self.db_user,
            "PWD": self.db_password,
        }

        url = URL.create(
            drivername=self.driver_name,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query=query,
        )
        return url