import datetime
import logging
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from socialapi.core.config import config
from socialapi.models.enums.token_type import TokenType

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])
ALGORITHM = "HS256"
DEFAULT_EXPIRE_TIME = 30
REFRESH_EXPIRE_DAYS = 1440 * 7  # 7 days
CONFIRMATION_EXPIRE_DAYS = 1440  # 1 day

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_jwt_token(
    email: str, type: str, expire_in_minutes: int = DEFAULT_EXPIRE_TIME
) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=expire_in_minutes
    )
    jwt_data = {"sub": email, "exp": expire, "type": type}
    return jwt.encode(jwt_data, key=config.JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(email: str, expire_in_minutes: int) -> str:
    return create_jwt_token(email, TokenType.ACCESS, expire_in_minutes)


def create_refresh_token(email: str) -> str:
    return create_jwt_token(email, TokenType.REFRESH, REFRESH_EXPIRE_DAYS)


def create_confirmation_token(email: str) -> str:
    return create_jwt_token(email, TokenType.CONFIRMATION, CONFIRMATION_EXPIRE_DAYS)


def decode_token(token: str) -> dict[str, Any]:
    decoded = jwt.decode(token=token, key=config.JWT_SECRET_KEY, algorithms=[ALGORITHM])
    return decoded


def get_password_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_password(plain_pwd, hashed_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)
