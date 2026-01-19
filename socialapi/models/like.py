from pydantic import BaseModel, ConfigDict


class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
