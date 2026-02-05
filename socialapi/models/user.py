from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    """Entidade principal do usuário. Contém todos os campos do banco."""

    id: int | None = None
    name: str
    email: str
    password: str | None = Field(default=None, exclude=True)
    confirmed: bool = False
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """DTO para criação de usuário via API."""

    name: str
    email: str
    password: str


class UserPatch(BaseModel):
    """DTO para atualização parcial de usuário."""

    name: Optional[str] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserConfirmation(BaseModel):
    email: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordReset(BaseModel):
    token: str
    new_password: str
