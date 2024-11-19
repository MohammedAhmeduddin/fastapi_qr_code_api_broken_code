# Load environment variables
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file to avoid hardcoding secrets in source code
load_dotenv()

# Environment Variables for Configuration

# Directory to save QR codes; defaults to './qr_codes' if not specified
QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))

# QR code colors
FILL_COLOR = os.getenv('FILL_COLOR', 'red')  # Color of the QR code
BACK_COLOR = os.getenv('BACK_COLOR', 'white')  # Background color of the QR code

# Server configuration
SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')  # Base URL of the server
SERVER_DOWNLOAD_FOLDER = os.getenv('SERVER_DOWNLOAD_FOLDER', 'downloads')  # Directory for downloads

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "secret-getenvkey")  # Cryptographic key for JWT tokens
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Algorithm for JWT encoding/decoding

# Token expiration settings
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Token validity duration in minutes

# Placeholder credentials for basic authentication
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')  # Admin username
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secret')  # Admin password
