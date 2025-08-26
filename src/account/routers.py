from typing import Annotated

from fastapi import APIRouter, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.account import schemas
from src.account.account_service import AccountService
from src.db import get_db_session

router = APIRouter(prefix="/account", tags=["Accounts"])

__oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/token")

def get_user_service(db: Annotated[AsyncSession, Depends(get_db_session)]):
    return AccountService(db)

@router.post("/token", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[AccountService, Depends(get_user_service)],
):
    return await user_service.authenticate_user(form_data.username, form_data.password)

@router.post("", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
async def create_user(
    user_schema: Annotated[schemas.UserCreateOrLogin, Form()],
    user_service: Annotated[AccountService, Depends(get_user_service)],
):
    return await user_service.create_user(user_schema)

@router.get("/me/", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_current_user(
    token: Annotated[str, Depends(__oauth2_scheme)],
    user_service: Annotated[AccountService, Depends(get_user_service)],
):
    return await user_service.get_current_user(token)
