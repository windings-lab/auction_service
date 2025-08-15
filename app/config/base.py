import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # openssl rand -hex 32
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "dangerous_secret_key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = os.getenv("TOKEN_EXPIRATION_IN_MINUTES", 30)

    @property
    def db_url(self) -> str:
        return "sqlite+aiosqlite:///./dev.db"
