from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def db_url(self) -> str:
        return "sqlite+aiosqlite:///./dev.db"
