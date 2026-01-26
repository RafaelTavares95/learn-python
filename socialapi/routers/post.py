import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from socialapi.models.comment import Comment
from socialapi.models.enums.post_sorting import PostSorting
from socialapi.models.post import (
    UserPost,
    UserPostIn,
    UserPostWithComments,
    UserPostWithLikes,
)
from socialapi.models.user import User
from socialapi.service.comment import find_comments_by_post_id
from socialapi.service.post import add_post, find_post_by_id, get_post, list_posts
from socialapi.service.user import get_user_from_token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(
    post: UserPostIn, current_user: Annotated[User, Depends(get_user_from_token)]
):
    return await add_post(post, current_user)


@router.get("/post", response_model=list[UserPostWithLikes])
async def list_all_posts(
    sort: PostSorting,
    current_user: Annotated[User, Depends(get_user_from_token)],
):
    return await list_posts(sort)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_full_post(
    post_id: int, current_user: Annotated[User, Depends(get_user_from_token)]
):
    if not await find_post_by_id(post_id):
        raise HTTPException(
            status_code=404, detail=f"Post with id: {post_id} not found"
        )
    return await get_post(post_id)


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def list_post_comments(
    post_id: int, current_user: Annotated[User, Depends(get_user_from_token)]
):
    if not await find_post_by_id(post_id):
        raise HTTPException(
            status_code=404, detail=f"Post with id: {post_id} not found"
        )

    return await find_comments_by_post_id(post_id)
