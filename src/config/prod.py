import os

from sqlalchemy.engine import URL
from sqlalchemy import util

from .base import Settings
from . import config

class ProdSettings(Settings):
    db_engine: str = config.get("database", "engine", fallback=os.getenv("DB_ENGINE", "postgres"))
    db_user: str | None = config.get("database", "user", fallback=os.getenv("DB_USER"))
    db_password: str | None = config.get("database", "password", fallback=os.getenv("DB_PASSWORD"))
    db_name: str = config.get("database", "name", fallback=os.getenv("DB_NAME", "db"))
    db_host: str = config.get("database", "host", fallback=os.getenv("DB_HOST", "localhost"))
    db_port: int = config.getint(
        "database", "port",
        fallback=int(os.getenv("DB_PORT") or (
        5432 if os.getenv("DB_ENGINE") == "postgres"
        else 3306 if os.getenv("DB_ENGINE") == "mysql"
        else 1433
    )))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.db_user is None:
            raise EnvironmentError("DB_USER environment variable is not set")

        if self.db_password is None:
            raise EnvironmentError("DB_PASSWORD environment variable is not set")

        if self.db_engine not in ("postgres", "mysql", "mssql"):
            raise EnvironmentError("DB_ENGINE must be 'postgres' or 'mysql' or 'mssql'")

    @property
    def db_url(self) -> URL:
        drivername = (
            "postgresql+asyncpg" if self.db_engine == "postgres" else
            "mysql+aiomysql" if self.db_engine == "mysql" else
            "mssql+aioodbc"
        )

        query = util.EMPTY_DICT
        if self.db_engine == "mssql":
            driver = config.get("mssql", "driver", fallback=os.getenv("MSSQL_DRIVER", None))
            if not driver:
                raise EnvironmentError("mssql driver variable not set. Specify in config.ini")
            query = {
                "driver": driver,
                "Trusted_Connection": "yes",
                "TrustServerCertificate": "yes",
            }
        url = URL.create(
            drivername=drivername,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query=query,
        )
        return url

_prod_settings = ProdSettings()