from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int | None = None
    name: str
    email: str


class UserIn(User):
    password: str
    model_config = ConfigDict(from_attributes=True)
