from socialapi.database import database, post_table
from socialapi.models.post import UserPost, UserPostIn, UserPostWithComments
from socialapi.service.comment import find_comments_by_post_id


async def add_post(post: UserPostIn):
    data = post.model_dump()
    query = post_table.insert().values(data)
    id = await database.execute(query)
    return {**data, "id": id}


async def get_post(id: int) -> UserPostWithComments:
    return UserPostWithComments(
        post=await find_post_by_id(id), comments=await find_comments_by_post_id(id)
    )


async def list_posts() -> list[UserPost]:
    query = post_table.select()
    return await database.fetch_all(query)


async def find_post_by_id(id: int):
    query = post_table.select().where(post_table.c.id == id)
    return await database.fetch_one(query)
