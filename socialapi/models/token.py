from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    confirmed_user: bool = False
    token_type: str | None = None


class LoginResponse(BaseModel):
    confirmed_user: bool = False


class RefreshResponse(BaseModel):
    status: str = "ok"


class RefreshRequest(BaseModel):
    refresh_token: str | None = None


class AccessTokenResponse(BaseModel):
    access_token: str | None = None
    token_type: str | None = None
