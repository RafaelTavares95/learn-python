from socialapi.models.post import UserPost, UserPostIn, UserPostWithComments
from socialapi.service.comment import find_comments_by_post_id

post_table = {}


def add_post(post: UserPostIn):
    data = post.model_dump()
    id = len(post_table)
    new_post = {"id": id, **data}
    post_table[id] = new_post
    return new_post


def get_post(id: int) -> UserPostWithComments:
    return UserPostWithComments(
        post=find_post_by_id(id), comments=find_comments_by_post_id(id)
    )


def list_posts() -> list[UserPost]:
    return list(post_table.values())


def find_post_by_id(id: int):
    return post_table.get(id)
