from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import model


class User(model.Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255))
