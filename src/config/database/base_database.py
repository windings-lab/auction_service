import os
from configparser import ConfigParser
from abc import ABC, abstractmethod

from sqlalchemy.engine import URL

class BaseDatabase(ABC):
    _registry: dict[str, type["BaseDatabase"]] = {}

    def __init__(self, config: ConfigParser):
        self.db_user: str | None = config.get("database", "user", fallback=os.getenv("DB_USER"))
        self.db_password: str | None = config.get("database", "password", fallback=os.getenv("DB_PASSWORD"))
        self.db_name: str = config.get("database", "name", fallback=os.getenv("DB_NAME", "db"))
        self.db_host: str = config.get("database", "host", fallback=os.getenv("DB_HOST", "localhost"))
        try:
            self.db_port: int | None = config.getint("database", "port", fallback=int(os.getenv("DB_PORT")))
        except TypeError:
            self.db_port = None

        if self.db_user is None:
            raise EnvironmentError("DB_USER environment variable is not set")

        if self.db_password is None:
            raise EnvironmentError("DB_PASSWORD environment variable is not set")

    def __init_subclass__(cls, *, engine: str, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDatabase._registry[engine] = cls

    @classmethod
    def create(cls, config: ConfigParser) -> "BaseDatabase":
        db_engine = config.get("database", "engine", fallback=os.getenv("DB_ENGINE"))

        try:
            return cls._registry[db_engine](config)
        except KeyError:
            raise ValueError(f"Unsupported database engine: {db_engine}")

    @abstractmethod
    def url(self) -> URL:
        pass