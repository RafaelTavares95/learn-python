import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient, logged_in_token: str):
    body = "First Post"
    expected_response = {"id": 1, "body": body}

    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert expected_response.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_without_body(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/post", json={}, headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_list_all_posts(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    response = await async_client.get(
        "/post", headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_get_post(
    async_client: AsyncClient,
    created_post: dict,
    created_comment: dict,
    logged_in_token: str,
):
    expected_full_post = {"post": created_post, "comments": [created_comment]}
    response = await async_client.get(
        f"/post/{created_post['id']}",
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 200
    assert response.json() == expected_full_post


@pytest.mark.anyio
async def test_get_post_with_unexistent_id(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    id = 123
    response = await async_client.get(
        f"/post/{id}", headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Post with id: {id} not found"


@pytest.mark.anyio
async def test_list_post_comments(
    async_client: AsyncClient, created_comment: dict, logged_in_token: str
):
    id = 1
    response = await async_client.get(
        f"/post/{id}/comment", headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_list_post_comments_with_unexistent_postid(
    async_client: AsyncClient,
    created_post: dict,
    created_comment: dict,
    logged_in_token: str,
):
    id = 123
    response = await async_client.get(
        f"/post/{id}/comment", headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Post with id: {id} not found"
