from fastapi import FastAPI
from app.config import QR_DIRECTORY
from app.routers import qr_code, oauth
from app.services.qr_service import create_directory
from app.utils.common import setup_logging

# Set up logging
setup_logging()

# Ensure QR code directory exists
create_directory(QR_DIRECTORY)

# Create the FastAPI app
app = FastAPI(
    title="QR Code Manager",
    description="A FastAPI application for creating, listing, and deleting QR codes with OAuth authentication.",
    version="0.0.1",
    redoc_url=None,
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

# Include routers
app.include_router(qr_code.router, prefix="/qr-codes", tags=["QR Codes"])
app.include_router(oauth.router, prefix="/auth", tags=["Authentication"])
