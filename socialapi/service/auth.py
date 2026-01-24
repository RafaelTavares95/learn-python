import logging

from jose import ExpiredSignatureError, JWTError

from socialapi.core.database import database, revoked_token_table
from socialapi.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from socialapi.exceptions.exceptions import CredentialException, UnauthorizedException
from socialapi.models.token import AccessTokenResponse, RefreshRequest, TokenResponse
from socialapi.models.user import UserLogin
from socialapi.service.user import find_user_by_email

logger = logging.getLogger(__name__)


async def autenticate_user(email: str, password: str):
    user = await find_user_by_email(email)
    if not user or not verify_password(password, user.password):
        raise CredentialException()
    return user


async def user_login(user: UserLogin) -> TokenResponse:
    autenticated_user = await autenticate_user(user.email, user.password)
    access_token = create_access_token(autenticated_user.email)
    refresh_token = create_refresh_token(autenticated_user.email)
    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


async def refresh_access_token(refresh: RefreshRequest) -> AccessTokenResponse:
    if await is_token_revoked(refresh.refresh_token):
        logger.warning(f"Refresh token is revoked: {refresh.refresh_token}")
        raise UnauthorizedException()

    try:
        email = decode_token(refresh.refresh_token)
        if email is None:
            raise UnauthorizedException()
        user = await find_user_by_email(email)
        if user is None:
            raise UnauthorizedException()
        access_token = create_access_token(user.email)
        return AccessTokenResponse(access_token=access_token, token_type="bearer")
    except ExpiredSignatureError as e:
        raise UnauthorizedException() from e
    except JWTError as e:
        raise UnauthorizedException() from e


async def revoke_token(token: str):
    logger.info("Revoking token")
    query = revoked_token_table.insert().values(token=token)
    await database.execute(query)


async def is_token_revoked(token: str):
    query = revoked_token_table.select().where(revoked_token_table.c.token == token)
    result = await database.fetch_one(query)
    return result is not None
