import logging

from fastapi import APIRouter, HTTPException

from socialapi.models.comment import Comment, CommentIn
from socialapi.service.comment import add_comment
from socialapi.service.post import find_post_by_id

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    if not await find_post_by_id(comment.post_id):
        raise HTTPException(
            status_code=404, detail=f"Post with id: {comment.post_id} not found"
        )

    return await add_comment(comment)
