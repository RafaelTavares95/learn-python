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
from socialapi.models.user import User, UserCreate, UserPatch

logger = logging.getLogger(__name__)


async def get_user_by_email(email: str) -> User | None:
    """Busca usuário por email. Retorna User ou None."""
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    return User.model_validate(result) if result else None


async def create_user(user: UserCreate) -> User:
    logger.info("Creating a new user")
    data = {
        "name": user.name,
        "email": user.email,
        "password": get_password_hash(user.password),
        "confirmed": False,
    }

    query = user_table.insert().values(data)
    user_id = await database.execute(query)

    return User(id=user_id, **data)


async def update_user(user_patch: UserPatch, current_user: User) -> User:
    data = user_patch.model_dump(exclude_unset=True)
    if "password" in data:
        data["password"] = get_password_hash(data["password"])

    if data:
        query = (
            user_table.update().where(user_table.c.id == current_user.id).values(data)
        )
        await database.execute(query)

    return User(
        id=current_user.id,
        name=data.get("name", current_user.name),
        email=current_user.email,
        password=current_user.password,
        confirmed=current_user.confirmed,
    )


async def set_user_confirmed(email: str):
    query = (
        user_table.update().where(user_table.c.email == email).values(confirmed=True)
    )
    await database.execute(query)


async def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        decoded = decode_token(token)
        if decoded.get("type") != TokenType.ACCESS:
            raise UnauthorizedException()

        email = decoded.get("sub")
        if not email:
            raise UnauthorizedException()

        user = await get_user_by_email(email)
        if not user:
            raise UnauthorizedException()

        return user
    except (ExpiredSignatureError, JWTError):
        raise UnauthorizedException()


async def get_user_for_resend_confirmation(email: str) -> User:
    """Busca usuário para reenvio de confirmação. Valida existência e status."""
    user = await get_user_by_email(email)
    if not user:
        raise UnauthorizedException(message="User not found")
    if user.confirmed:
        raise UnauthorizedException(message="User is already confirmed")
    return user
