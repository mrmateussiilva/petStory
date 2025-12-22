"""Email service for sending PDFs via Resend."""

import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via Resend."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize email service.
        
        Args:
            api_key: Resend API key. If None, uses settings.RESEND_API_KEY
        """
        self.api_key = api_key or settings.RESEND_API_KEY
        self.from_email = settings.EMAIL_FROM
        self.from_name = settings.EMAIL_FROM_NAME
        
        # Initialize Resend client if API key is provided
        if self.api_key:
            try:
                from resend import Resend
                self.client = Resend(api_key=self.api_key)
                self.enabled = True
            except Exception as e:
                logger.warning(f"Failed to initialize Resend client: {e}")
                self.enabled = False
        else:
            self.enabled = False
            logger.info("Resend API key not provided, email service will log only")

    async def send_pdf(
        self, to_email: str, subject: str, pdf_bytes: bytes, pdf_filename: str = "petstory_coloring_book.pdf"
    ) -> bool:
        """Send PDF via email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            pdf_bytes: PDF file as bytes
            pdf_filename: Name for the PDF attachment
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            if not self.enabled:
                # Simulate sending (log only)
                logger.info(
                    f"[SIMULATED] Would send email to {to_email} "
                    f"with PDF ({len(pdf_bytes)} bytes) as {pdf_filename}"
                )
                logger.info(f"[SIMULATED] Subject: {subject}")
                return True
            
            # Send via Resend
            params = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": [to_email],
                "subject": subject,
                "attachments": [
                    {
                        "filename": pdf_filename,
                        "content": pdf_bytes,
                    }
                ],
                "html": """
                <html>
                    <body style="font-family: Arial, sans-serif; padding: 20px;">
                        <h2>Seu livro de colorir PetStory está pronto! 🎨</h2>
                        <p>Olá!</p>
                        <p>Seu livro de colorir personalizado com seus pets foi gerado com sucesso.</p>
                        <p>Você pode encontrar o PDF anexado neste email.</p>
                        <p>Divirta-se colorindo! 🐾</p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">
                            PetStory - Transformando memórias em arte
                        </p>
                    </body>
                </html>
                """,
            }
            
            email = self.client.emails.send(params)
            logger.info(f"Email sent successfully to {to_email}, ID: {email.get('id', 'N/A')}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}", exc_info=True)
            return False

