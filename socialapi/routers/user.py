from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from socialapi.models.token import TokenResponse
from socialapi.models.user import User, UserIn, UserLogin, UserPatch
from socialapi.service.user import (
    create_user,
    find_user_by_email,
    get_user_from_token,
    update_user,
    user_login,
)

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserIn):
    if await find_user_by_email(user.email):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return await create_user(user)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await user_login(
        UserLogin(email=form_data.username, password=form_data.password)
    )


@router.get("/user")
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
