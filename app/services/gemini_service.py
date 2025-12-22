"""Gemini Image Generation implementation using the new API."""

import base64
import io
import logging
from typing import Optional

import google.generativeai as genai
from PIL import Image

from app.core.config import settings
from app.interfaces.image_generator import ImageGenerator

logger = logging.getLogger(__name__)


class GeminiGenerator(ImageGenerator):
    """Gemini Image Generation implementation of ImageGenerator.
    
    Uses the new Gemini image generation API (Nano Banana / Nano Banana Pro).
    See: https://ai.google.dev/gemini-api/docs/image-generation
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """Initialize Gemini client.
        
        Args:
            api_key: Gemini API key. If None, uses settings.GEMINI_API_KEY
            model_name: Model name. If None, uses settings.GEMINI_IMAGE_MODEL
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model_name = model_name or settings.GEMINI_IMAGE_MODEL
        self.model = genai.GenerativeModel(self.model_name)

    async def generate(self, image_bytes: bytes, prompt: str) -> bytes:
        """Generate a coloring book style image from input photo.
        
        Args:
            image_bytes: Input image as bytes
            prompt: Text prompt for transformation
            
        Returns:
            Generated image as PNG bytes
            
        Raises:
            Exception: If generation fails
        """
        try:
            # Load image from bytes
            input_image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary (remove alpha channel)
            if input_image.mode != "RGB":
                input_image = input_image.convert("RGB")
            
            # Generate image using Gemini
            # The API supports image-to-image transformation
            response = self.model.generate_content(
                [prompt, input_image],
                generation_config={
                    "temperature": 0.4,
                },
            )
            
            # Extract generated image from response
            if not response.candidates or not response.candidates[0].content.parts:
                raise ValueError("No image generated in response")
            
            # The response contains parts, and one of them should be the generated image
            # According to documentation: https://ai.google.dev/gemini-api/docs/image-generation
            generated_image = None
            for part in response.candidates[0].content.parts:
                # Method 1: Check if part has text (shouldn't happen for image generation, but log it)
                if hasattr(part, 'text') and part.text:
                    logger.debug(f"Response part contains text: {part.text[:100]}")
                
                # Method 2: Check if part has inline_data (base64 encoded image)
                if hasattr(part, 'inline_data') and part.inline_data:
                    try:
                        # Decode base64 image
                        image_data = base64.b64decode(part.inline_data.data)
                        generated_image = Image.open(io.BytesIO(image_data))
                        logger.debug("Extracted image from inline_data")
                        break
                    except Exception as e:
                        logger.warning(f"Failed to decode inline_data: {e}")
                        continue
                
                # Method 3: Check if part has as_image method (PIL Image)
                if hasattr(part, 'as_image'):
                    try:
                        generated_image = part.as_image()
                        logger.debug("Extracted image using as_image() method")
                        break
                    except Exception as e:
                        logger.debug(f"as_image() method failed: {e}")
                        continue
                
                # Method 4: Check if part is directly an image
                if isinstance(part, Image.Image):
                    generated_image = part
                    logger.debug("Part is directly an Image")
                    break
            
            if generated_image is None:
                # Log all available attributes for debugging
                logger.error("Available parts attributes:")
                for i, part in enumerate(response.candidates[0].content.parts):
                    logger.error(f"Part {i}: {type(part)}, attributes: {dir(part)}")
                raise ValueError("No image data found in response parts")
            
            # Convert to RGB and save as PNG bytes
            if generated_image.mode != "RGB":
                generated_image = generated_image.convert("RGB")
            
            output_buffer = io.BytesIO()
            generated_image.save(output_buffer, format="PNG")
            output_bytes = output_buffer.getvalue()
            
            logger.info(f"Successfully generated image ({len(output_bytes)} bytes)")
            return output_bytes
            
        except Exception as e:
            logger.error(f"Error generating image with Gemini: {str(e)}", exc_info=True)
            raise

