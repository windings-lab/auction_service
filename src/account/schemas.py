from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str

class UserCreateOrLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)
