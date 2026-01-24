from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from socialapi.models.token import AccessTokenResponse, RefreshRequest, TokenResponse
from socialapi.models.user import UserLogin
from socialapi.service.auth import refresh_access_token, revoke_token, user_login

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await user_login(
        UserLogin(email=form_data.username, password=form_data.password)
    )


@router.post(
    "/refresh", response_model=AccessTokenResponse, status_code=status.HTTP_200_OK
)
async def refresh(refresh: RefreshRequest):
    return await refresh_access_token(refresh)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(refresh: RefreshRequest):
    await revoke_token(refresh.refresh_token)
