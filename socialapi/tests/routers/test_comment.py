import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_comment(
    async_client: AsyncClient,
    created_post: dict,
    created_user: dict,
    logged_in_token: str,
):
    body = "First Comment"
    expected_response = {
        "id": 1,
        "body": body,
        "post_id": created_post["id"],
        "user_id": created_user["id"],
    }

    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert expected_response.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_comment_for_unexisted_post(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    body = "First Comment"

    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": 123},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 404
