from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import logging

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES  # Application-specific settings
from app.schema import Token  # Token response model
from app.utils.common import authenticate_user, create_access_token

# Initialize logging for debugging purposes
logging.basicConfig(level=logging.INFO)

# OAuth2 setup with the endpoint for obtaining tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create an API router
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint for user login and token generation.
    """
    logging.info("Attempting to authenticate user.")

    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logging.warning(f"Authentication failed for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )

    logging.info(f"Token successfully generated for user: {user['username']}")
    return {"access_token": access_token, "token_type": "bearer"}
