"""
This module contains test cases for the FastAPI application, including
login and QR code operations.
"""

import pytest
from httpx import AsyncClient
from app.main import app

BASE_URL = "http://test"
TEST_USER_CREDENTIALS = {"username": "admin", "password": "secret"}

@pytest.mark.asyncio
async def test_login_for_access_token():
    """
    Tests the /auth/token endpoint for generating an access token.
    """
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/auth/token", data=TEST_USER_CREDENTIALS)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_create_qr_code_unauthorized():
    """
    Tests that creating a QR code without authentication returns a 401 status code.
    """
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/qr-codes/", json=qr_request)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_and_delete_qr_code():
    """
    Tests creating and deleting a QR code with authentication.
    """
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        # Obtain access token
        token_response = await client.post("/auth/token", data=TEST_USER_CREDENTIALS)
        access_token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create QR code
        qr_request = {
            "url": "https://example.com",
            "fill_color": "red",
            "back_color": "white",
            "size": 10,
        }
        create_response = await client.post("/qr-codes/", json=qr_request, headers=headers)
        assert create_response.status_code in [201, 409]

        # Delete QR code if it was created
        if create_response.status_code == 201:
            qr_code_url = create_response.json()["qr_code_url"]
            qr_filename = qr_code_url.split('/')[-1]
            delete_response = await client.delete(f"/qr-codes/{qr_filename}", headers=headers)
            assert delete_response.status_code == 204
