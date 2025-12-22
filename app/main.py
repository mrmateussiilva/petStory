"""FastAPI application main entry point."""

import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.interfaces.image_generator import ImageGenerator
from app.services.email_service import EmailService
from app.services.gemini_service import GeminiGenerator
from app.worker import process_pet_photos

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global instances (initialized in lifespan)
image_generator: ImageGenerator = None
email_service: EmailService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global image_generator, email_service
    
    # Initialize services on startup
    logger.info("Initializing services...")
    try:
        image_generator = GeminiGenerator()
        email_service = EmailService()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {e}", exc_info=True)
        raise
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API para transformar fotos de pets em desenhos de colorir",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for frontend (GitHub Pages)
# In debug mode, allow all origins for easier development
cors_origins = ["*"] if settings.DEBUG else settings.cors_origins_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/upload")
async def upload_pet_photos(
    background_tasks: BackgroundTasks,
    email: str,
    files: List[UploadFile] = File(...),
):
    """Upload multiple pet photos for processing.
    
    Args:
        background_tasks: FastAPI background tasks
        email: Recipient email address
        files: List of uploaded image files
        
    Returns:
        JSON response with job status
    """
    # Validate email
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    # Validate files
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="At least one image file is required")
    
    if len(files) > 20:  # Reasonable limit
        raise HTTPException(
            status_code=400, detail="Maximum 20 images allowed per request"
        )
    
    # Validate file types and read images
    images = []
    allowed_content_types = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
    
    for file in files:
        if file.content_type not in allowed_content_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. "
                f"Allowed types: {', '.join(allowed_content_types)}",
            )
        
        try:
            image_bytes = await file.read()
            if len(image_bytes) == 0:
                raise HTTPException(
                    status_code=400, detail=f"File {file.filename} is empty"
                )
            
            # Validate image size (max 10MB per image)
            if len(image_bytes) > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} exceeds 10MB limit",
                )
            
            images.append(image_bytes)
            logger.info(f"Loaded image: {file.filename} ({len(image_bytes)} bytes)")
            
        except Exception as e:
            logger.error(f"Error reading file {file.filename}: {e}", exc_info=True)
            raise HTTPException(
                status_code=400, detail=f"Error reading file {file.filename}: {str(e)}"
            )
    
    # Add background task
    background_tasks.add_task(
        process_pet_photos,
        images=images,
        email=email,
        image_generator=image_generator,
        email_service=email_service,
    )
    
    logger.info(
        f"Background task queued: {len(images)} images for {email}"
    )
    
    return JSONResponse(
        status_code=202,
        content={
            "status": "accepted",
            "message": f"Processing {len(images)} image(s). You will receive an email at {email} when ready.",
            "images_count": len(images),
            "email": email,
        },
    )

