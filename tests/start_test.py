import pytest
from httpx import AsyncClient
from app.main import app  # Import the FastAPI app

BASE_URL = "http://test"
TEST_USER_CREDENTIALS = {
    "username": "admin",
    "password": "secret",
}

@pytest.mark.asyncio
async def test_login_for_access_token():
    """
    Test user login and token generation.
    Ensures the /token endpoint returns a valid access token and token type.
    """
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/token", data=TEST_USER_CREDENTIALS)
    
    # Assertions
    assert response.status_code == 200, "Login failed: Invalid credentials"
    response_json = response.json()
    assert "access_token" in response_json, "Access token not found in response"
    assert response_json["token_type"] == "bearer", "Invalid token type"


@pytest.mark.asyncio
async def test_create_qr_code_unauthorized():
    """
    Test QR code creation without authentication.
    Ensures the /qr-codes/ endpoint returns 401 Unauthorized when no token is provided.
    """
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/qr-codes/", json=qr_request)
    
    # Assertions
    assert response.status_code == 401, "Unauthorized access should return status 401"


@pytest.mark.asyncio
async def test_create_and_delete_qr_code():
    """
    Test authenticated QR code creation and deletion.
    Ensures the user can:
    1. Login and retrieve an access token.
    2. Create a QR code using the token.
    3. Delete the QR code successfully.
    """
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        # Step 1: Login and retrieve access token
        token_response = await client.post("/token", data=TEST_USER_CREDENTIALS)
        assert token_response.status_code == 200, "Login failed"
        access_token = token_response.json().get("access_token")
        assert access_token, "Access token not returned"
        headers = {"Authorization": f"Bearer {access_token}"}

        # Step 2: Create a QR code
        qr_request = {
            "url": "https://example.com",
            "fill_color": "red",
            "back_color": "white",
            "size": 10,
        }
        create_response = await client.post("/qr-codes/", json=qr_request, headers=headers)
        assert create_response.status_code in [201, 409], "QR code creation failed"
        
        # If the QR code was created, attempt to delete it
        if create_response.status_code == 201:
            qr_code_url = create_response.json().get("qr_code_url")
            assert qr_code_url, "QR code URL not returned"
            
            qr_filename = qr_code_url.split('/')[-1]
            delete_response = await client.delete(f"/qr-codes/{qr_filename}", headers=headers)
            assert delete_response.status_code == 204, "Failed to delete QR code"
