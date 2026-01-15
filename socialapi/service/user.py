import logging

from jose import ExpiredSignatureError, JWTError

from socialapi.core.database import database, user_table
from socialapi.core.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from socialapi.exceptions.exceptions import CredentialException, UnauthorizedException
from socialapi.models.token import TokenResponse
from socialapi.models.user import User, UserIn, UserLogin

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


async def autenticate_user(email: str, password: str):
    user = await find_user_by_email(email)
    if not user or not verify_password(password, user.password):
        raise CredentialException()
    return user


async def user_login(user: UserLogin) -> TokenResponse:
    autenticated_user = await autenticate_user(user.email, user.password)
    access_token = create_access_token(autenticated_user.email, 30)
    return TokenResponse(access_token=access_token, token_type="bearer")


async def get_user_from_token(token: str) -> User:
    try:
        email = decode_token(token)
        if email is None:
            raise UnauthorizedException()
        user = await find_user_by_email(email)
        if user is None:
            raise UnauthorizedException()
        return User(**user)
    except ExpiredSignatureError or JWTError as e:
        raise UnauthorizedException() from e
