import logging
from typing import Annotated

from fastapi import Depends
from jose import ExpiredSignatureError, JWTError

from socialapi.core.database import database, user_table
from socialapi.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    oauth2_scheme,
    verify_password,
)
from socialapi.exceptions.exceptions import CredentialException, UnauthorizedException
from socialapi.models.token import AccessTokenResponse, RefreshRequest, TokenResponse
from socialapi.models.user import User, UserIn, UserLogin, UserPatch

logger = logging.getLogger(__name__)


async def find_user_by_email(email: str):
    logger.info("Finding user by email", extra={"email": email})
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result


async def create_user(user: UserIn):
    logger.info("Creating a new user")
    data = user.model_dump()
    data["password"] = get_password_hash(data["password"])
    query = user_table.insert().values(data)
    id = await database.execute(query)
    logger.debug(f"User created with id={id}", extra={"email": data["email"]})
    return User(id=id, name=data["name"], email=data["email"])


async def update_user(user: UserPatch, current_user: User):
    logger.info("Update user data")
    data = user.model_dump(exclude_unset=True)
    if "password" in data and data["password"]:
        data["password"] = get_password_hash(data["password"])

    if data:
        query = (
            user_table.update().where(user_table.c.id == current_user.id).values(data)
        )
        await database.execute(query)

    # Return updated user info
    return User(
        id=current_user.id,
        name=data.get("name", current_user.name),
        email=current_user.email,
    )


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


async def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        email = decode_token(token)
        if email is None:
            raise UnauthorizedException()
        user = await find_user_by_email(email)
        if user is None:
            raise UnauthorizedException()
        return User(**user)
    except ExpiredSignatureError as e:
        raise UnauthorizedException() from e
    except JWTError as e:
        raise UnauthorizedException() from e


async def refresh_access_token(refresh: RefreshRequest) -> AccessTokenResponse:
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
