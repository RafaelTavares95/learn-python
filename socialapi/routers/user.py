from fastapi import APIRouter, HTTPException, status

from socialapi.models.token import TokenResponse
from socialapi.models.user import User, UserIn, UserLogin
from socialapi.service.user import create_user, find_user_by_email, user_login

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
async def login(user: UserLogin):
    return await user_login(user)
