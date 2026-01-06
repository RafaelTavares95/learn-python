import logging

from socialapi.database import comment_table, database
from socialapi.models.comment import CommentIn

logger = logging.getLogger(__name__)


async def add_comment(comment: CommentIn):
    logger.info("Creating a new comment")
    data = comment.model_dump()
    query = comment_table.insert().values(data)
    id = await database.execute(query)
    logger.debug(f"Comment created with id: {id}")
    return {**data, "id": id}


async def find_comments_by_post_id(post_id: int):
    logger.info(f"Finding comments by post_id: {post_id}")
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)
