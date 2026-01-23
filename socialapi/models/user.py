from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int | None = None
    name: str
    email: str


class UserIn(User):
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str


class UserPatch(BaseModel):
    name: Optional[str]
    password: Optional[str] = None
