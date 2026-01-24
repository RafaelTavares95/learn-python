import datetime
import logging

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from socialapi.core.config import config

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])
ALGORITHM = "HS256"
DEFAULT_EXPIRE_TIME = 30
REFRESH_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(
    email: str, expire_in_minutes: int = DEFAULT_EXPIRE_TIME
) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=expire_in_minutes
    )
    jwt_data = {"sub": email, "exp": expire}
    return jwt.encode(jwt_data, key=config.JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(email: str) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        days=REFRESH_EXPIRE_DAYS
    )
    jwt_data = {"sub": email, "exp": expire}
    return jwt.encode(jwt_data, key=config.JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    decoded = jwt.decode(token=token, key=config.JWT_SECRET_KEY, algorithms=[ALGORITHM])
    return decoded.get("sub")


def get_password_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_password(plain_pwd, hashed_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)
