from fastapi import FastAPI
from app.config import QR_DIRECTORY
from app.routers import qr_code, oauth  # Ensure these imports match your project structure
from app.services.qr_service import create_directory
from app.utils.common import setup_logging

# Set up logging for the application
setup_logging()

# Ensure the directory for storing QR codes exists; create it if it doesn't
create_directory(QR_DIRECTORY)

# Create the FastAPI application instance with metadata
app = FastAPI(
    title="QR Code Manager",
    description=(
        "A FastAPI application for creating, listing, and deleting QR codes. "
        "It also supports OAuth for secure access."
    ),
    version="0.0.1",
    redoc_url=None,  # Disable ReDoc
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Include application routers for handling QR code management and OAuth authentication
app.include_router(qr_code.router, prefix="/qr", tags=["QR Code Management"])
app.include_router(oauth.router, prefix="/auth", tags=["Authentication"])
