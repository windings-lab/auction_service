import os
from .base import Settings

class ProdSettings(Settings):
    pg_user: str | None = os.getenv("PGUSER")
    pg_password: str | None = os.getenv("PGPASSWORD")
    pg_database: str = os.getenv("PGDATABASE", "db")
    pg_host: str = os.getenv("PGHOST", "localhost")
    pg_port: int = int(os.getenv("PGPORT", "5432"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.pg_user is None:
            raise EnvironmentError("PGUSER environment variable is not set")

        if self.pg_password is None:
            raise EnvironmentError("PGPASSWORD environment variable is not set")

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@"
            f"{self.pg_host}:{self.pg_port}/{self.pg_database}"
        )

_prod_settings = ProdSettings()
