from socialapi.database import comment_table, database
from socialapi.models.comment import CommentIn


async def add_comment(comment: CommentIn):
    data = comment.model_dump()
    query = comment_table.insert().values(data)
    id = await database.execute(query)
    return {**data, "id": id}


async def find_comments_by_post_id(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)
