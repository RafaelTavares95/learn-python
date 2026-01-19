import logging

from socialapi.core.database import database, like_table
from socialapi.models.user import User

logger = logging.getLogger(__name__)


async def likePost(post_id: int, user: User):
    logger.info(f"Like in post with id: {post_id} by user: {user.id}")
    data = {"post_id": post_id, "user_id": user.id}
    query = like_table.insert().values(data)
    id = await database.execute(query)
    return {**data, "id": id}
