from fastapi import APIRouter, HTTPException

from socialapi.models.comment import Comment, CommentIn
from socialapi.service.comment import add_comment
from socialapi.service.post import find_post_by_id

router = APIRouter()


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    if not find_post_by_id(comment.post_id):
        raise HTTPException(status_code=404, detail="Post not found")

    return add_comment(comment)
