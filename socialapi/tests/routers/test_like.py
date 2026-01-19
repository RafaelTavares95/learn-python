import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_like_post(
    async_client: AsyncClient,
    created_post: dict,
    created_user: dict,
    logged_in_token: str,
):
    expected_response = {
        "id": 1,
        "post_id": created_post["id"],
        "user_id": created_user["id"],
    }

    response = await async_client.post(
        "/like",
        json={"post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert expected_response.items() <= response.json().items()


@pytest.mark.anyio
async def test_like_unexisted_post(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    response = await async_client.post(
        "/like",
        json={"post_id": 123},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 404
