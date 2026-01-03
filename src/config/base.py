import configparser
import os

from pydantic import PrivateAttr
from pydantic_settings import BaseSettings

from .database.base_database import BaseDatabase


class Settings(BaseSettings):
    _config: configparser.ConfigParser = PrivateAttr()

    # openssl rand -hex 32
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "dangerous_secret_key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = os.getenv("TOKEN_EXPIRATION_IN_MINUTES", 30)

    _database: BaseDatabase = PrivateAttr()

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config = config
        self._database = BaseDatabase.create(self._config)

    @property
    def database(self):
        return self._database

    @property
    def config(self):
        return self._config

    @staticmethod
    def create():
        config = configparser.ConfigParser()
        config.read("config.ini")

        env = config.get("app", "settings", fallback=os.getenv("APP_SETTINGS", "dev").lower())

        if env == "dev":
            from .dev import DevSettings
            return DevSettings(config, _env_file='.env', _env_file_encoding='utf-8')
        elif env == "prod":
            from .prod import ProdSettings
            return ProdSettings(config)
        else:
            raise EnvironmentError("APP_SETTINGS environment variable is not set")


