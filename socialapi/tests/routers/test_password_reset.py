import re
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from socialapi.core.security import decode_token
from socialapi.models.enums.token_type import TokenType


@pytest.mark.anyio
async def test_password_reset_request_flow(
    async_client: AsyncClient, mock_send_email: AsyncMock, created_user: dict
):
    # 1. Request password reset
    email = created_user["email"]
    response = await async_client.post("/password-reset-request", json={"email": email})

    assert response.status_code == 204

    # 2. Verify email was sent
    assert mock_send_email.called
    args, kwargs = mock_send_email.call_args
    assert args[0] == email
    assert args[1] == "Resete sua senha"

    body = args[2]
    # Extract token from the URL in the body
    # Link format: .../reset-password/{token}
    match = re.search(r"reset-password/([a-zA-Z0-9\._\-]+)", body)
    assert match is not None
    token = match.group(1)

    # 3. Decode token and verify it's correct
    decoded = decode_token(token)
    assert decoded["sub"] == email
    assert decoded["type"] == TokenType.RESET_PASSWORD

    # Optional: verify expiration is around 15 minutes (hard to test precisely due to time passing, but we can check if it's within a range)
    import datetime

    exp = decoded["exp"]
    now = datetime.datetime.now(datetime.UTC).timestamp()
    # It should expire in roughly 15 minutes (900 seconds)
    assert exp > now
    assert exp - now <= 15 * 60 + 10  # Allow small buffer


@pytest.mark.anyio
async def test_password_reset_request_non_existent_email(
    async_client: AsyncClient, mock_send_email: AsyncMock
):
    # Request password reset for email that doesn't exist
    response = await async_client.post(
        "/password-reset-request", json={"email": "nonexistent@example.com"}
    )

    # Security: should still return 204
    assert response.status_code == 204
    # But email should NOT be sent (or at least our current logic doesn't send it)
    assert not mock_send_email.called
