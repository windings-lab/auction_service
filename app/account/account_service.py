import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.db_service import DBService

from . import schemas
from . import models
from .auth_context import AuthContext


class AccountService(DBService):
    """Thread-safe"""
    auth_context: AuthContext = AuthContext()

    async def create_user(self, user_schema: schemas.UserCreateOrLogin):
        user_schema.password = self.auth_context.get_password_hash(user_schema.password)
        new_user = models.User(**user_schema.model_dump())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def get_user(self, username: str) -> models.User:
        result = await self.db.execute(select(models.User).where(models.User.username == username))

        try:
            user: models.User = result.scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {username} not found"
            )

        return user

    async def get_current_user(self, token: str) -> models.User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.auth_context.jwt_secret_key,
                algorithms=[self.auth_context.jwt_algorithm]
            )
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = schemas.TokenData(username=username)

            user = await self.get_user(token_data.username)
        except (InvalidTokenError, HTTPException):
            raise credentials_exception

        return user

    async def authenticate_user(self, username: str, password: str) -> schemas.Token:
        try:
            user = await self.get_user(username)
        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.detail,
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not self.auth_context.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.auth_context.create_access_token(payload={"sub": user.username})

        return schemas.Token(access_token=access_token, token_type="bearer")