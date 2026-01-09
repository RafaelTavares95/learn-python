import logging

from socialapi.core.database import database, user_table
from socialapi.models.user import User, UserIn

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
    query = user_table.insert().values(data)
    id = await database.execute(query)
    logger.debug(f"User created with id={id}", extra={"email": data["email"]})
    return User(id=id, name=data["name"], email=data["email"])
