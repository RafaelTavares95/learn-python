import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_user_register(async_client: AsyncClient):
    expected_response = {"id": 1, "name": "test", "email": "teste@email.com"}

    response = await async_client.post(
        "/register",
        json={"name": "test", "email": "teste@email.com", "password": "1234"},
    )

    assert response.status_code == 201
    assert expected_response.items() <= response.json().items()


@pytest.mark.anyio
async def test_user_register_without_name(async_client: AsyncClient):
    response = await async_client.post(
        "/register",
        json={"email": "teste@email.com", "password": "1234"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_user_register_with_existing_email(
    async_client: AsyncClient, created_user: dict
):
    response = await async_client.post(
        "/register",
        json={"name": "test", "email": created_user["email"], "password": "1234"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"


@pytest.mark.anyio
async def test_get_user(
    async_client: AsyncClient, created_user: dict, logged_in_token: str
):
    response = await async_client.get(
        "/user",
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == created_user["email"]
    assert response.json()["name"] == created_user["name"]


@pytest.mark.anyio
async def test_get_user_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/user")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_update_user(
    async_client: AsyncClient, created_user: dict, logged_in_token: str
):
    new_data = {"name": "Updated Name"}
    response = await async_client.patch(
        "/user",
        json=new_data,
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["email"] == created_user["email"]


@pytest.mark.anyio
async def test_update_user_unauthorized(async_client: AsyncClient):
    response = await async_client.patch("/user", json={"name": "New Name"})
    assert response.status_code == 401


@pytest.mark.anyio
async def test_update_user_password(
    async_client: AsyncClient, created_user: dict, logged_in_token: str
):
    new_data = {"password": "newpassword"}
    response = await async_client.patch(
        "/user",
        json=new_data,
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 200

    # Verify we can login with the new password
    login_response = await async_client.post(
        "/login",
        data={"username": created_user["email"], "password": "newpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
