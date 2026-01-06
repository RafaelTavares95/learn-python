import logging

from fastapi import APIRouter, HTTPException

from socialapi.models.comment import Comment
from socialapi.models.post import UserPost, UserPostIn, UserPostWithComments
from socialapi.service.comment import find_comments_by_post_id
from socialapi.service.post import add_post, find_post_by_id, get_post, list_posts

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    return await add_post(post)


@router.get("/post", response_model=list[UserPost])
async def list_all_posts():
    return await list_posts()


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_full_post(post_id: int):
    if not await find_post_by_id(post_id):
        logger.error(f"Post with id: {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")
    return await get_post(post_id)


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def list_post_comments(post_id: int):
    if not await find_post_by_id(post_id):
        logger.error(f"Post with id: {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")

    return await find_comments_by_post_id(post_id)
