import re
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_full_email_confirmation_flow(
    async_client: AsyncClient, mock_send_email: AsyncMock
):
    # 1. Register a new user
    email = "flowtest@example.com"
    register_response = await async_client.post(
        "/register",
        json={"name": "Flow Test", "email": email, "password": "password123"},
    )
    assert register_response.status_code == 201

    # 2. Verify email was "sent"
    assert mock_send_email.called
    args, kwargs = mock_send_email.call_args
    # args: (to, subject, body), kwargs: {html: ...}
    assert args[0] == email
    assert args[1] == "Confirm your email"

    body = args[2]
    # Extract token from the URL in the body
    # Link format: .../confirm-email/{token}
    match = re.search(r"confirm-email/([a-zA-Z0-9\._\-]+)", body)
    assert match is not None
    token = match.group(1)

    # 3. Confirm the email using the token
    # Note: The route in auth.py is /confirm/{token} (not /confirm-email/{token})
    # But the service creates a URL for the FRONTEND.
    # Usually the frontend would then call the backend.
    # In our tests, we call the backend /confirm/{token} directly.
    confirm_response = await async_client.get(f"/confirm/{token}")
    assert confirm_response.status_code == 200
    assert confirm_response.json()["message"] == "Email confirmed successfully"

    # 4. Verify user is now confirmed
    login_response = await async_client.post(
        "/login",
        data={"username": email, "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    # login returns LoginResponse(confirmed_user=...)
    # We need to check if it's true now.
    # Wait, in auth.py: return LoginResponse(confirmed_user=token_response.confirmed_user)
    assert login_response.json()["confirmed_user"] is True


@pytest.mark.anyio
async def test_resend_confirmation_email(
    async_client: AsyncClient, mock_send_email: AsyncMock
):
    # 1. Register a user
    email = "resend@example.com"
    await async_client.post(
        "/register",
        json={"name": "Resend Test", "email": email, "password": "password123"},
    )

    # Clear the mock calls from the registration
    mock_send_email.reset_mock()

    # 2. Call resend endpoint
    resend_response = await async_client.post(
        "/resend-confirmation", json={"email": email}
    )
    assert resend_response.status_code == 204

    # 3. Verify email was "sent" again
    assert mock_send_email.called
    args, _ = mock_send_email.call_args
    assert args[0] == email
    assert args[1] == "Confirm your email"


@pytest.mark.anyio
async def test_resend_confirmation_already_confirmed(
    async_client: AsyncClient, mock_send_email: AsyncMock
):
    # 1. Register and confirm user
    email = "already@example.com"
    await async_client.post(
        "/register",
        json={"name": "Already Test", "email": email, "password": "password123"},
    )

    # Get token and confirm
    _, _, body = mock_send_email.call_args[0]
    token = re.search(r"confirm-email/([a-zA-Z0-9\._\-]+)", body).group(1)
    await async_client.get(f"/confirm/{token}")

    # 2. Reset mock and try resending
    mock_send_email.reset_mock()
    resend_response = await async_client.post(
        "/resend-confirmation", json={"email": email}
    )

    # It should fail because user is already confirmed
    assert resend_response.status_code == 401
    assert resend_response.json()["detail"] == "User is already confirmed"
    assert not mock_send_email.called
