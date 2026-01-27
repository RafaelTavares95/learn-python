import pytest
from httpx import AsyncClient

from socialapi.core.security import create_confirmation_token
from socialapi.service.user import find_user_by_email


@pytest.mark.anyio
async def test_user_login(async_client: AsyncClient, created_user: dict):
    response = await async_client.post(
        "/login",
        data={"username": created_user["email"], "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_user_login_fail(async_client: AsyncClient, created_user: dict):
    response = await async_client.post(
        "/login",
        data={"username": created_user["email"], "password": "12345"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "One of your information is wrong, please verify your email or password."
    )


@pytest.mark.anyio
async def test_refresh_token(async_client: AsyncClient, created_user: dict):
    # Login to get refresh token
    login_response = await async_client.post(
        "/login",
        data={"username": created_user["email"], "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh access token
    refresh_response = await async_client.post(
        "/refresh",
        json={"refresh_token": refresh_token},
    )

    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
    assert refresh_response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_refresh_token_invalid(async_client: AsyncClient):
    refresh_response = await async_client.post(
        "/refresh",
        json={"refresh_token": "invalid_token"},
    )

    assert refresh_response.status_code == 401


@pytest.mark.anyio
async def test_logout_and_refresh_fail(async_client: AsyncClient, created_user: dict):
    # Login to get refresh token
    login_response = await async_client.post(
        "/login",
        data={"username": created_user["email"], "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Logout
    logout_response = await async_client.post(
        "/logout",
        json={"refresh_token": refresh_token},
    )
    assert logout_response.status_code == 204

    # Try to refresh access token using the revoked refresh token
    refresh_response = await async_client.post(
        "/refresh",
        json={"refresh_token": refresh_token},
    )

    assert refresh_response.status_code == 401


@pytest.mark.anyio
async def test_confirm_user(async_client: AsyncClient, created_user: dict):
    user = await find_user_by_email(created_user["email"])
    confirmation_token = create_confirmation_token(created_user["email"])

    assert user["confirmed"] is False
    response = await async_client.get(f"/confirm/{confirmation_token}")
    assert response.status_code == 200

    user = await find_user_by_email(created_user["email"])
    assert user["confirmed"] is True


@pytest.mark.anyio
async def test_confirm_user_invalid_token(async_client: AsyncClient):
    response = await async_client.get("/confirm/invalid_token")
    assert response.status_code == 401
