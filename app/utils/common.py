import logging.config
import os
import base64
from typing import List
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
from app.config import ADMIN_PASSWORD, ADMIN_USER, ALGORITHM, SECRET_KEY
import validators
from urllib.parse import urlparse, urlunparse

# Load environment variables
load_dotenv()

# Debug: Print environment variable values
print("ADMIN_USER:", os.getenv("ADMIN_USER"))
print("ADMIN_PASSWORD:", os.getenv("ADMIN_PASSWORD"))
print("SECRET_KEY:", os.getenv("SECRET_KEY"))

# Ensure critical environment variables are loaded
assert os.getenv("ADMIN_USER"), "ADMIN_USER is not set"
assert os.getenv("ADMIN_PASSWORD"), "ADMIN_PASSWORD is not set"
assert os.getenv("SECRET_KEY"), "SECRET_KEY is not set"

def setup_logging():
    """
    Sets up logging for the application using a configuration file.
    """
    try:
        logging_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logging.conf')
        normalized_path = os.path.normpath(logging_config_path)
        logging.config.fileConfig(normalized_path, disable_existing_loggers=False)
    except Exception as e:
        logging.error(f"Failed to configure logging: {e}")

def authenticate_user(username: str, password: str):
    """
    Authenticates a user by checking credentials against environment variables.
    """
    expected_username = os.getenv("ADMIN_USER")
    expected_password = os.getenv("ADMIN_PASSWORD")

    if username == expected_username and password == expected_password:
        logging.info(f"User authenticated: {username}")
        return {"username": username}

    logging.warning(f"Authentication failed for user: {username}")
    return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a JWT access token with an optional expiration time.
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logging.debug(f"Access token created: {encoded_jwt}")
        return encoded_jwt
    except Exception as e:
        logging.error(f"Failed to create access token: {e}")
        raise

def decode_filename_to_url(encoded_str: str) -> str:
    """
    Decodes a base64 encoded string back into a URL, adding necessary padding.
    """
    try:
        padding_needed = 4 - (len(encoded_str) % 4)
        encoded_str += "=" * padding_needed
        decoded_bytes = base64.urlsafe_b64decode(encoded_str)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        logging.error(f"Failed to decode filename to URL: {e}")
        raise
