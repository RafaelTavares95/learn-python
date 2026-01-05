from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from socialapi.main import app
from socialapi.service.comment import comment_table
from socialapi.service.post import post_table

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
    post_table.clear()
    comment_table.clear()
    yield


# Create a async client
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac


# Specific setups


async def create_post(body: str, ac: AsyncClient) -> dict:
    response = await ac.post("/post", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, ac: AsyncClient) -> dict:
    response = await ac.post("/comment", json={"body": body, "post_id": post_id})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("First Post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("First Comment", created_post["id"], async_client)
