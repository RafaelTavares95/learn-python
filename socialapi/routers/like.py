import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from socialapi.models.like import PostLike, PostLikeIn
from socialapi.models.user import User
from socialapi.service.like import likePost
from socialapi.service.post import find_post_by_id
from socialapi.service.user import get_user_from_token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/like", response_model=PostLike, status_code=201)
async def register_like(
    like: PostLikeIn, current_user: Annotated[User, Depends(get_user_from_token)]
):
    if not await find_post_by_id(like.post_id):
        raise HTTPException(
            status_code=404, detail=f"Post with id: {like.post_id} not found"
        )

    return await likePost(like.post_id, current_user)
