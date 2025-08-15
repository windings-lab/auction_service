from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext

from app.config import settings


class AuthContext:
    """Thread-safe"""
    _instance: "AuthContext" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.jwt_secret_key = settings.jwt_secret_key
        self.cryptography_algorithm = settings.cryptography_algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(self, payload: dict):
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, self.jwt_secret_key, algorithm=self.cryptography_algorithm)
        return encoded_jwt