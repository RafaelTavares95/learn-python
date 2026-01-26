import logging

import sqlalchemy
from sqlalchemy import func

from socialapi.core.database import database, like_table, post_table
from socialapi.models.enums.post_sorting import PostSorting
from socialapi.models.post import (
    UserPostIn,
    UserPostWithComments,
    UserPostWithLikes,
)
from socialapi.models.user import User
from socialapi.service.comment import find_comments_by_post_id

logger = logging.getLogger(__name__)

post_likes_view = (
    sqlalchemy.select(
        post_table,
        func.count(like_table.c.post_id).label("likes"),
    )
    .select_from(post_table.outerjoin(like_table))
    .group_by(post_table.c.id)
)


async def add_post(post: UserPostIn, user: User):
    logger.info("Creating a new post")
    data = {**post.model_dump(), "user_id": user.id}
    query = post_table.insert().values(data)
    id = await database.execute(query)
    logger.debug(f"Post created with id: {id}", extra={"received_data": data})
    return {**data, "id": id}


async def get_post(id: int) -> UserPostWithComments:
    logger.info(f"Getting a complete post with id: {id}")
    return UserPostWithComments(
        post=await select_post_with_likes(id),
        comments=await find_comments_by_post_id(id),
    )


async def list_posts(sort: PostSorting = PostSorting.NEWEST) -> list[UserPostWithLikes]:
    logger.info(f"Getting all posts sorted by {sort}")

    match sort:
        case PostSorting.NEWEST:
            query = post_likes_view.order_by(post_table.c.created_at.desc())
        case PostSorting.OLDEST:
            query = post_likes_view.order_by(post_table.c.created_at.asc())
        case PostSorting.MOST_LIKED:
            query = post_likes_view.order_by(sqlalchemy.desc("likes"))
        case PostSorting.LEAST_LIKED:
            query = post_likes_view.order_by(sqlalchemy.asc("likes"))

    return await database.fetch_all(query)


async def find_post_by_id(id: int):
    logger.info(f"Finding post with id: {id}")
    query = post_table.select().where(post_table.c.id == id)
    return await database.fetch_one(query)


async def select_post_with_likes(id: int) -> UserPostWithLikes:
    logger.info(f"Getting post with likes with id: {id}")
    query = post_likes_view.where(post_table.c.id == id)
    return await database.fetch_one(query)
