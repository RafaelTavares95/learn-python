import logging
from typing import Annotated

from fastapi import Depends
from jose import ExpiredSignatureError, JWTError

from socialapi.core.database import database, user_table
from socialapi.core.security import (
    decode_token,
    get_password_hash,
    oauth2_scheme,
)
from socialapi.exceptions.exceptions import UnauthorizedException
from socialapi.models.enums.token_type import TokenType
from socialapi.models.user import User, UserIn, UserPatch

logger = logging.getLogger(__name__)


async def find_user_by_email(email: str) -> dict:
    logger.info("Finding user by email", extra={"email": email})
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result


async def create_user(user: UserIn) -> User:
    logger.info("Creating a new user")
    data = user.model_dump()
    data["password"] = get_password_hash(data["password"])
    data.setdefault("confirmed", False)
    query = user_table.insert().values(data)
    id = await database.execute(query)
    logger.debug(f"User created with id={id}", extra={"email": data["email"]})
    return User(
        id=id, name=data["name"], email=data["email"], confirmed=data["confirmed"]
    )


async def update_user(user: UserPatch, current_user: User) -> User:
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
        confirmed=current_user.confirmed,
    )


async def set_user_confirmed(email: str):
    logger.info("Confirming user")
    query = (
        user_table.update().where(user_table.c.email == email).values(confirmed=True)
    )
    await database.execute(query)


async def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        decoded = decode_token(token)
    except ExpiredSignatureError as e:
        raise UnauthorizedException() from e
    except JWTError as e:
        raise UnauthorizedException() from e

    if decoded.get("type") != TokenType.ACCESS:
        raise UnauthorizedException()

    email = decoded.get("sub")
    if email is None:
        raise UnauthorizedException()

    user = await find_user_by_email(email)
    if user is None:
        raise UnauthorizedException()

    return User(**user)
