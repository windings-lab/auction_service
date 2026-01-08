import os
from configparser import ConfigParser
from abc import ABC, abstractmethod

from sqlalchemy.engine import URL

class BaseDatabase(ABC):
    _registry: dict[str, type["BaseDatabase"]] = {}

    def __init__(self):
        self.db_user: str | None = os.getenv("DB_USER")
        self.db_password: str | None = os.getenv("DB_PASSWORD")
        self.db_name: str = os.getenv("DB_NAME", "db")
        self.db_host: str = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT")
        self.db_port: int | None = int(db_port) if db_port else None

        if self.db_user is None:
            raise EnvironmentError("DB_USER environment variable is not set")

        if self.db_password is None:
            raise EnvironmentError("DB_PASSWORD environment variable is not set")

    def __init_subclass__(cls, *, engine: str, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDatabase._registry[engine] = cls

    @classmethod
    def create(cls) -> "BaseDatabase":
        db_engine = os.getenv("DB_ENGINE", "sqlite")

        try:
            return cls._registry[db_engine]()
        except KeyError:
            raise ValueError(f"Unsupported database engine: {db_engine}")

    @abstractmethod
    def url(self) -> URL:
        pass