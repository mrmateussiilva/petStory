"""QR Code generation service."""

import base64
import logging
from io import BytesIO

import qrcode
from PIL import Image

logger = logging.getLogger(__name__)


class QRCodeService:
    """Service for generating QR codes."""

    def __init__(self):
        """Initialize QR code service."""
        pass

    def generate_qr_code(
        self, url: str, size: int = 200, border: int = 4, box_size: int = 10
    ) -> Image.Image:
        """Generate QR code image.

        Args:
            url: URL to encode in QR code
            size: Size of QR code image in pixels (final output size)
            border: Border size in boxes (default: 4)
            box_size: Size of each box in pixels (default: 10)

        Returns:
            PIL Image of QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # 15% error correction
            box_size=box_size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Criar imagem
        img = qr.make_image(fill_color="black", back_color="white")

        # Redimensionar para o tamanho desejado
        if size != (box_size * 21 + border * 2 * box_size):  # Tamanho padrão
            img = img.resize((size, size), Image.Resampling.LANCZOS)

        logger.debug(f"QR code generated for URL: {url[:50]}... (size: {size}x{size})")
        return img

    def generate_qr_code_bytes(self, url: str, size: int = 200, format: str = "PNG") -> bytes:
        """Generate QR code as bytes.

        Args:
            url: URL to encode
            size: Size in pixels
            format: Image format (PNG, JPEG, etc.)

        Returns:
            QR code image as bytes
        """
        img = self.generate_qr_code(url, size)
        buffer = BytesIO()
        img.save(buffer, format=format)
        return buffer.getvalue()

    def generate_qr_code_base64(
        self, url: str, size: int = 200, format: str = "PNG"
    ) -> str:
        """Generate QR code as base64 string for embedding in HTML.

        Args:
            url: URL to encode
            size: Size in pixels
            format: Image format

        Returns:
            Base64 encoded string (data URI ready)
        """
        qr_bytes = self.generate_qr_code_bytes(url, size, format)
        base64_str = base64.b64encode(qr_bytes).decode("utf-8")
        mime_type = f"image/{format.lower()}"
        return f"data:{mime_type};base64,{base64_str}"

