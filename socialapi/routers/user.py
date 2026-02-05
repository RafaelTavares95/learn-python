from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from socialapi.models.user import User, UserCreate, UserPatch
from socialapi.service.email import send_confirmation_email
from socialapi.service.user import (
    create_user,
    get_user_by_email,
    get_user_from_token,
    update_user,
)

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, background_tasks: BackgroundTasks):
    if await get_user_by_email(user.email):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    created_user = await create_user(user)
    send_confirmation_email(created_user, background_tasks)
    return created_user


@router.get("/user", response_model=User)
async def get_user_by_token(
    current_user: Annotated[User, Depends(get_user_from_token)],
):
    return current_user


@router.patch("/user", response_model=User, status_code=status.HTTP_200_OK)
async def update(
    user: UserPatch,
    current_user: Annotated[User, Depends(get_user_from_token)],
):
    return await update_user(user, current_user)
