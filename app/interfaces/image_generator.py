"""Abstract interface for image generation services."""

from abc import ABC, abstractmethod


class ImageGenerator(ABC):
    """Abstract base class for image generation services.
    
    This follows the Strategy pattern, allowing easy substitution
    of different AI image generation providers.
    """

    @abstractmethod
    async def generate(
        self, image_bytes: bytes, prompt: str
    ) -> bytes:
        """Generate a transformed image from input image bytes.
        
        Args:
            image_bytes: The input image as bytes (JPEG, PNG, etc.)
            prompt: The text prompt describing the desired transformation
            
        Returns:
            The generated image as bytes (typically PNG or JPEG)
            
        Raises:
            Exception: If image generation fails
        """
        pass

