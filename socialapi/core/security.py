import datetime
import logging

from jose import jwt
from passlib.context import CryptContext

from socialapi.core.config import config

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])
ALGORITHM = "HS256"


def create_access_token(email: str, expire_in_minutes: int) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=expire_in_minutes
    )
    jwt_data = {"sub": email, "exp": expire}
    return jwt.encode(jwt_data, key=config.JWT_SECRET_KEY, algorithm=ALGORITHM)


def get_password_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_password(plain_pwd, hashed_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)
