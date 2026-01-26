from pydantic import BaseModel, ConfigDict

from socialapi.models.comment import Comment


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int


class UserPostWithLikes(UserPost):
    likes: int


class UserPostWithComments(BaseModel):
    post: UserPostWithLikes
    comments: list[Comment]
