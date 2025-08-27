import os

from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    # openssl rand -hex 32
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "dangerous_secret_key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = os.getenv("TOKEN_EXPIRATION_IN_MINUTES", 30)

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername="sqlite+aiosqlite",
            database="dev.db",
        )
