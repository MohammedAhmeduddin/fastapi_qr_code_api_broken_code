# conftest.py
import pytest
from httpx import AsyncClient
from app.main import app  # Adjust import path as necessary

@pytest.fixture
async def client():
    """
    Provides an AsyncClient instance for making HTTP requests in tests.
    The client is initialized with the FastAPI app and a base URL.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture
async def get_access_token_for_test(client):
    """
    Retrieves an access token for testing authenticated endpoints.
    Uses the default admin credentials to request a token from the /token endpoint.
    """
    form_data = {"username": "admin", "password": "secret"}
    response = await client.post("/token", data=form_data)
    response.raise_for_status()  # Ensure the request was successful
    return response.json()["access_token"]
