import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # openssl rand -hex 32
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", "dangerous_secret_key")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes = os.getenv("TOKEN_EXPIRATION_IN_MINUTES", 30)

    @property
    def db_url(self) -> str:
        return "sqlite+aiosqlite:///./dev.db"
