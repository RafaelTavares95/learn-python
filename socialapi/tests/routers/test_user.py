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
