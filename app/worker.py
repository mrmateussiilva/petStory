"""Background worker for processing pet photos into coloring book PDFs."""

import asyncio
import logging
import time
from typing import List, Optional

from app.core.config import settings
from app.interfaces.image_generator import ImageGenerator
from app.services.email_service import EmailService
from app.services.pdf_service import PDFService

logger = logging.getLogger(__name__)

# Prompt para geração de imagens estilo Bobbie Goods
COLORING_BOOK_PROMPT = (
    "Line art coloring page style Bobbie Goods of a cute pet, "
    "thick uniform lines, no shading, pure white background, "
    "minimal details suitable for children coloring book"
)


async def process_pet_photos(
    images: List[bytes],
    email: str,
    image_generator: ImageGenerator,
    pdf_service: Optional[PDFService] = None,
    email_service: Optional[EmailService] = None,
) -> dict:
    """Process multiple pet photos into a coloring book PDF and send via email.
    
    Args:
        images: List of image bytes (pet photos)
        email: Recipient email address
        image_generator: Image generator service (injected dependency)
        pdf_service: PDF service instance (optional, creates if None)
        email_service: Email service instance (optional, creates if None)
        
    Returns:
        Dictionary with processing results
    """
    pdf_service = pdf_service or PDFService()
    email_service = email_service or EmailService()
    
    generated_images = []
    errors = []
    
    logger.info(f"Starting processing of {len(images)} images for {email}")
    
    # Process each image
    for idx, image_bytes in enumerate(images, 1):
        try:
            logger.info(f"Processing image {idx}/{len(images)}")
            
            # Generate coloring book style image
            generated_image = await image_generator.generate(
                image_bytes, COLORING_BOOK_PROMPT
            )
            generated_images.append(generated_image)
            
            logger.info(f"Successfully generated image {idx}/{len(images)}")
            
            # Sleep between generations to avoid rate limits
            if idx < len(images):  # Don't sleep after last image
                await asyncio.sleep(settings.WORKER_SLEEP_SECONDS)
                
        except Exception as e:
            error_msg = f"Error processing image {idx}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            errors.append({"image_index": idx, "error": str(e)})
            # Continue processing other images
    
    if not generated_images:
        error_msg = "No images were successfully generated"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "errors": errors,
            "images_processed": 0,
            "images_total": len(images),
        }
    
    # Create PDF from generated images
    try:
        logger.info(f"Creating PDF from {len(generated_images)} images")
        pdf_bytes = pdf_service.create_pdf_from_images(generated_images)
        
        if not pdf_bytes:
            raise ValueError("PDF generation returned empty bytes")
        
        logger.info(f"PDF created successfully ({len(pdf_bytes)} bytes)")
        
    except Exception as e:
        error_msg = f"Error creating PDF: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "errors": errors,
            "images_processed": len(generated_images),
            "images_total": len(images),
        }
    
    # Send email with PDF
    try:
        logger.info(f"Sending PDF to {email}")
        email_sent = await email_service.send_pdf(
            to_email=email,
            subject="Seu livro de colorir PetStory está pronto! 🎨",
            pdf_bytes=pdf_bytes,
        )
        
        if not email_sent:
            raise ValueError("Email service returned False")
        
        logger.info(f"Successfully sent email to {email}")
        
    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "errors": errors,
            "images_processed": len(generated_images),
            "images_total": len(images),
            "pdf_created": True,
        }
    
    # Success!
    return {
        "success": True,
        "images_processed": len(generated_images),
        "images_total": len(images),
        "errors": errors,
        "email": email,
    }

