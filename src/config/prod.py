import os
from .base import Settings

class ProdSettings(Settings):
    db_engine: str = os.getenv("DB_ENGINE", "postgres")  # "postgres" or "mysql"
    db_user: str | None = os.getenv("DB_USER")
    db_password: str | None = os.getenv("DB_PASSWORD")
    db_name: str = os.getenv("DB_NAME", "db")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT") or (5432 if os.getenv("DB_ENGINE", "postgres") == "postgres" else 3306))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.db_user is None:
            raise EnvironmentError("DB_USER environment variable is not set")

        if self.db_password is None:
            raise EnvironmentError("DB_PASSWORD environment variable is not set")

        if self.db_engine not in ("postgres", "mysql"):
            raise EnvironmentError("DB_ENGINE must be 'postgres' or 'mysql'")

    @property
    def db_url(self) -> str:
        if self.db_engine == "postgres":
            return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        else:  # mysql
            return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

_prod_settings = ProdSettings()