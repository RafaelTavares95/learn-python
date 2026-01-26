import pytest
from httpx import AsyncClient

from socialapi.core.security import create_access_token


@pytest.mark.anyio
async def test_create_post(
    async_client: AsyncClient, created_user: dict, logged_in_token: str
):
    body = "First Post"
    expected_response = {"id": 1, "body": body, "user_id": created_user["id"]}

    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert expected_response.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_without_token(async_client: AsyncClient):
    body = "First Post"

    response = await async_client.post("/post", json={"body": body})

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.anyio
async def test_create_post_invalid_token(async_client: AsyncClient):
    body = "First Post"

    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": "Bearer 1235"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid access token."


@pytest.mark.anyio
async def test_create_post_expired_token(async_client: AsyncClient, created_user: dict):
    token = create_access_token("teste@email.com", expire_in_minutes=-1)
    body = "First Post"
    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid access token."


@pytest.mark.anyio
async def test_create_post_without_body(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/post", json={}, headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 422


@pytest.mark.anyio
@pytest.mark.parametrize(
    "sort_param, expected_order_idx",
    [
        ("newest", [2, 1, 0]),
        ("oldest", [0, 1, 2]),
        ("most_liked", [1, 2, 0]),
        ("least_liked", [2, 0, 1]),
    ],
)
async def test_list_all_posts_sorting(
    async_client: AsyncClient,
    created_post: dict,
    logged_in_token: str,
    sort_param: str,
    expected_order_idx: list[int],
):
    # Post 2
    response = await async_client.post(
        "/post",
        json={"body": "Second Post"},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    post_2 = response.json()

    # Like Post 2
    await async_client.post(
        "/like",
        json={"post_id": post_2["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    # Post 3
    response = await async_client.post(
        "/post",
        json={"body": "Third Post"},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    post_3 = response.json()

    posts = [
        {**created_post, "likes": 0},
        {**post_2, "likes": 1},
        {**post_3, "likes": 0},
    ]

    response = await async_client.get(
        "/post",
        headers={"Authorization": f"Bearer {logged_in_token}"},
        params={"sort": sort_param},
    )

    assert response.status_code == 200
    expected = [posts[i] for i in expected_order_idx]
    assert response.json() == expected


@pytest.mark.anyio
async def test_list_all_posts_missing_sort(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.get(
        "/post", headers={"Authorization": f"Bearer {logged_in_token}"}
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_list_all_posts_invalid_sort(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.get(
        "/post",
        headers={"Authorization": f"Bearer {logged_in_token}"},
        params={"sort": "invalid"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_post(
    async_client: AsyncClient,
    created_post: dict,
    created_comment: dict,
    logged_in_token: str,
):
    expected_full_post = {
        "post": {**created_post, "likes": 0},
        "comments": [created_comment],
    }
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


@pytest.mark.anyio
async def test_get_post_likes(
    async_client: AsyncClient,
    created_post: dict,
    registred_like: dict,
    logged_in_token: str,
):
    expected_full_post = {
        "post": {**created_post, "likes": 1},
        "comments": [],
    }
    response = await async_client.get(
        f"/post/{created_post['id']}",
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 200
    assert response.json() == expected_full_post
