from jose import jwt

from socialapi.core import security
from socialapi.core.config import config
from socialapi.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


def test_get_hashed_password():
    password = "1234"
    hashed_password = get_password_hash(password)
    assert hashed_password != password


def test_verify_password():
    password = "1234"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)


def test_create_access_token():
    email = "teste@test.com"
    token = create_access_token(email=email, expire_in_minutes=30)
    decoded = jwt.decode(
        token=token, key=config.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    assert email == decoded.get("sub")
