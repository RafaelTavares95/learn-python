import logging

from socialapi.database import database, post_table
from socialapi.models.post import UserPost, UserPostIn, UserPostWithComments
from socialapi.service.comment import find_comments_by_post_id

logger = logging.getLogger(__name__)


async def add_post(post: UserPostIn):
    logger.info("Creating a new post")
    data = post.model_dump()
    query = post_table.insert().values(data)
    id = await database.execute(query)
    logger.debug(f"Post created with id: {id}")
    return {**data, "id": id}


async def get_post(id: int) -> UserPostWithComments:
    logger.info(f"Getting a complete post with id: {id}")
    return UserPostWithComments(
        post=await find_post_by_id(id), comments=await find_comments_by_post_id(id)
    )


async def list_posts() -> list[UserPost]:
    logger.info("Getting all posts")
    query = post_table.select()
    return await database.fetch_all(query)


async def find_post_by_id(id: int):
    logger.info(f"Finding post with id: {id}")
    query = post_table.select().where(post_table.c.id == id)
    return await database.fetch_one(query)
