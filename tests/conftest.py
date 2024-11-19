"""
This module provides pytest fixtures for testing the FastAPI application.
"""

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    """
    Provides an instance of AsyncClient for making HTTP requests in tests.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def get_access_token_for_test(test_client: AsyncClient):  # Renamed parameter to test_client
    """
    Provides an access token for authenticated endpoints during tests.
    """
    form_data = {"username": "admin", "password": "secret"}
    response = await test_client.post("/auth/token", data=form_data)  # Updated to test_client
    response.raise_for_status()
    return response.json()["access_token"]
