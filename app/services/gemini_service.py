"""Gemini Imagen 3 implementation for image generation."""

import io
import logging
from typing import Optional

import google.generativeai as genai
import requests
from PIL import Image

from app.core.config import settings
from app.interfaces.image_generator import ImageGenerator

logger = logging.getLogger(__name__)


class GeminiGenerator(ImageGenerator):
    """Gemini Imagen 3 implementation of ImageGenerator."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client.
        
        Args:
            api_key: Gemini API key. If None, uses settings.GEMINI_API_KEY
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("imagen-3.0-generate-001")

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
            response = self.model.generate_content(
                [prompt, input_image],
                generation_config={
                    "temperature": 0.4,
                    "top_p": 0.95,
                    "top_k": 40,
                },
            )
            
            # Extract generated image
            if not response.candidates or not response.candidates[0].content.parts:
                raise ValueError("No image generated in response")
            
            generated_image = response.candidates[0].content.parts[0]
            
            # Download the image
            image_url = generated_image.url
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            # Convert to bytes
            output_image = Image.open(io.BytesIO(img_response.content))
            
            # Convert to RGB and save as PNG bytes
            if output_image.mode != "RGB":
                output_image = output_image.convert("RGB")
            
            output_buffer = io.BytesIO()
            output_image.save(output_buffer, format="PNG")
            output_bytes = output_buffer.getvalue()
            
            logger.info(f"Successfully generated image ({len(output_bytes)} bytes)")
            return output_bytes
            
        except Exception as e:
            logger.error(f"Error generating image with Gemini: {str(e)}", exc_info=True)
            raise

