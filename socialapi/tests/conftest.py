import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

os.environ["ENV_STATE"] = "test"

from socialapi.core.database import database, engine, metadata
from socialapi.main import app

# Using fixture we can create a setup for our tests and prepare functions to be injected by pytest


# Define the async module usec
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# Create a TestClient
@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


# Clears the data whenever tests have been run.
@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield
    await database.disconnect()


# Create a async client
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac


# Specific setups


async def create_post(body: str, ac: AsyncClient, logged_in_token: str) -> dict:
    response = await ac.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_comment(
    body: str, post_id: int, ac: AsyncClient, logged_in_token: str
) -> dict:
    response = await ac.post(
        "/comment",
        json={"body": body, "post_id": post_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_user(name: str, email: str, password: str, ac: AsyncClient) -> dict:
    response = await ac.post(
        "/register", json={"name": name, "email": email, "password": password}
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient, logged_in_token: str):
    return await create_post("First Post", async_client, logged_in_token)


@pytest.fixture()
async def created_comment(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    return await create_comment(
        "First Comment", created_post["id"], async_client, logged_in_token
    )


@pytest.fixture()
async def created_user(async_client: AsyncClient):
    return await create_user("test", "teste@email.com", "1234", async_client)


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, created_user) -> str:
    response = await async_client.post(
        "/login", json={"email": "teste@email.com", "password": "1234"}
    )
    return response.json()["access_token"]
