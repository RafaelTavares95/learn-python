import logging
from typing import Annotated

from fastapi import Depends
from jose import ExpiredSignatureError, JWTError

from socialapi.core.config import config
from socialapi.core.database import database, user_table
from socialapi.core.security import (
    create_confirmation_token,
    decode_token,
    get_password_hash,
    oauth2_scheme,
)
from socialapi.core.tasks import send_email
from socialapi.exceptions.exceptions import MailResponseException, UnauthorizedException
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

    await send_email_confirmation(data["email"])

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


async def create_confirmation_url(email: str):
    return f"{config.FRONTEND_URL}/confirm-email/{create_confirmation_token(email)}"


async def send_email_confirmation(email: str):
    user = await find_user_by_email(email)
    if user is None:
        raise UnauthorizedException(message="User not found")

    if user.confirmed:
        raise UnauthorizedException(message="User is already confirmed")

    confirmation_url = await create_confirmation_url(email)
    try:
        await send_email(
            email,
            "Confirm your email",
            (
                f"Hello, {user.name}!\n\n"
                f"Confirm your email by clicking the link below: {confirmation_url}\n\n"
                f"If you did not create this account, please ignore this email.\n\n"
                f"Best regards,\n"
                f"{config.APP_NAME}"
            ),
            html=(
                f"<html>"
                f"<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>"
                f"<div style='max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;'>"
                f"<h2 style='color: #4A90E2;'>Hello, {user.name}!</h2>"
                f"<p>Thank you for signing up! Please confirm your email address to activate your account.</p>"
                f"<div style='margin: 30px 0;'>"
                f"<a href='{confirmation_url}' style='background-color: #4A90E2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;'>Confirm Email Address</a>"
                f"</div>"
                f"<p style='font-size: 0.9em; color: #666;'>If the button above doesn't work, copy and paste this link into your browser:</p>"
                f"<p style='font-size: 0.9em; color: #666;'>{confirmation_url}</p>"
                f"<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>"
                f"<p>If you did not create this account, please ignore this email.</p>"
                f"<p>Best regards,<br><strong>{config.APP_NAME} Team</strong></p>"
                f"</div>"
                f"</body>"
                f"</html>"
            ),
        )
    except MailResponseException as e:
        logger.error(f"Error sending email: {e}")
