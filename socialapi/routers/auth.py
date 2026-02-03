from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from socialapi.core.config import config
from socialapi.exceptions.exceptions import UnauthorizedException
from socialapi.models.token import (
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
)
from socialapi.models.user import PasswordResetRequest, UserConfirmation, UserLogin
from socialapi.service.auth import (
    confirm_email_from_token,
    refresh_access_token,
    revoke_token,
    user_login,
)
from socialapi.service.user import (
    send_email_confirmation,
    send_password_reset_email,
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
):
    token_response = await user_login(
        UserLogin(email=form_data.username, password=form_data.password)
    )
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="lax",
    )
    return LoginResponse(confirmed_user=token_response.confirmed_user)


@router.post("/refresh", response_model=RefreshResponse, status_code=status.HTTP_200_OK)
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise UnauthorizedException(message="Refresh token missing")

    token_response = await refresh_access_token(
        RefreshRequest(refresh_token=refresh_token)
    )
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="lax",
    )
    return RefreshResponse()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await revoke_token(refresh_token)

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")


@router.get("/confirm/{token}")
async def confirm_user(token: str):
    await confirm_email_from_token(token)
    return {"message": "Email confirmed successfully"}


@router.post("/resend-confirmation", status_code=status.HTTP_204_NO_CONTENT)
async def resend_confirmation(userConfirmation: UserConfirmation):
    return await send_email_confirmation(userConfirmation.email)


@router.post("/password-reset-request", status_code=status.HTTP_204_NO_CONTENT)
async def password_reset_request(reset_request: PasswordResetRequest):
    await send_password_reset_email(reset_request.email)
