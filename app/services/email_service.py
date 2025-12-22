"""Email service for sending PDFs via SMTP (native Python)."""

import logging
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP."""

    def __init__(
        self,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
    ):
        """Initialize email service.
        
        Args:
            smtp_server: SMTP server address. If None, uses settings.SMTP_SERVER
            smtp_port: SMTP server port. If None, uses settings.SMTP_PORT
            smtp_user: SMTP username. If None, uses settings.SMTP_USER
            smtp_password: SMTP password. If None, uses settings.SMTP_PASSWORD
        """
        self.smtp_server = smtp_server or settings.SMTP_SERVER
        self.smtp_port = smtp_port or settings.SMTP_PORT
        self.smtp_user = smtp_user or settings.SMTP_USER
        self.smtp_password = smtp_password or settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM
        self.from_name = settings.EMAIL_FROM_NAME
        
        # Check if SMTP is configured
        if self.smtp_user and self.smtp_password:
            self.enabled = True
            logger.info(f"Email service initialized with SMTP server: {self.smtp_server}:{self.smtp_port}")
        else:
            self.enabled = False
            logger.info("SMTP credentials not provided, email service will log only")

    async def send_pdf(
        self, to_email: str, subject: str, pdf_bytes: bytes, pdf_filename: str = "livro_pet.pdf"
    ) -> bool:
        """Send PDF via email using SMTP.
        
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
            
            # Create multipart message
            msg = MIMEMultipart("mixed")
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            msg["Subject"] = subject
            
            # Create HTML body
            body_html = """
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
            """
            
            # Attach HTML body
            msg.attach(MIMEText(body_html, "html", "utf-8"))
            
            # Attach PDF
            pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
            pdf_attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=pdf_filename,
            )
            msg.attach(pdf_attachment)
            
            # Connect to SMTP server and send
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                    # Enable debug (optional, can be removed in production)
                    if settings.DEBUG:
                        server.set_debuglevel(1)
                    
                    # Start TLS encryption
                    server.starttls()
                    
                    # Login
                    server.login(self.smtp_user, self.smtp_password)
                    
                    # Send email
                    server.send_message(msg)
                    
                logger.info(f"Email sent successfully to {to_email}")
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"SMTP authentication failed: {str(e)}")
                return False
            except smtplib.SMTPException as e:
                logger.error(f"SMTP error occurred: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error sending email: {str(e)}", exc_info=True)
                return False
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}", exc_info=True)
            return False
    
    async def send_pet_story_email(
        self,
        to_email: str,
        pet_name: str,
        pdf_bytes: bytes,
        html_content: str,
        pdf_filename: str = "kit_digital.pdf",
    ) -> bool:
        """Send pet story email with PDF and HTML attachments.
        
        Args:
            to_email: Recipient email address
            pet_name: Pet's name (for subject)
            pdf_bytes: PDF file as bytes
            html_content: HTML content for the tribute page
            pdf_filename: Name for the PDF attachment
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            if not self.enabled:
                # Simulate sending (log only)
                logger.info(
                    f"[SIMULATED] Would send pet story email to {to_email} "
                    f"for {pet_name} with PDF ({len(pdf_bytes)} bytes) and HTML"
                )
                return True
            
            # Create multipart message
            msg = MIMEMultipart("mixed")
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            msg["Subject"] = f"O Kit Digital de {pet_name} está pronto! 🎨🐾"
            
            # Create HTML body
            body_html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                        <h2 style="color: #7c3aed;">🎉 O Kit Digital do {pet_name} está pronto!</h2>
                        <p>Olá!</p>
                        <p>Ficamos felizes em compartilhar que o kit digital personalizado do <strong>{pet_name}</strong> foi criado com sucesso!</p>
                        <p>Você encontrará anexos:</p>
                        <ul>
                            <li><strong>PDF do Kit Digital</strong> - com capa, biografia, página para colorir e adesivos</li>
                            <li><strong>Página Web de Homenagem</strong> - uma página HTML linda que você pode compartilhar ou guardar</li>
                        </ul>
                        <p>Divirta-se colorindo e compartilhando as memórias do {pet_name}! 🐾</p>
                        <hr style="margin: 30px 0; border: none; border-top: 1px solid #e0e0e0;">
                        <p style="color: #666; font-size: 12px; text-align: center;">
                            PetStory - Transformando memórias em arte<br>
                            Criado com ❤️ para você
                        </p>
                    </div>
                </body>
            </html>
            """
            
            # Attach HTML body
            msg.attach(MIMEText(body_html, "html", "utf-8"))
            
            # Attach PDF
            pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
            pdf_attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=pdf_filename,
            )
            msg.attach(pdf_attachment)
            
            # Attach HTML file
            html_attachment = MIMEText(html_content, "html", "utf-8")
            html_attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=f"homenagem_{pet_name.replace(' ', '_')}.html",
            )
            msg.attach(html_attachment)
            
            # Connect to SMTP server and send
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                    # Enable debug (optional, can be removed in production)
                    if settings.DEBUG:
                        server.set_debuglevel(1)
                    
                    # Start TLS encryption
                    server.starttls()
                    
                    # Login
                    server.login(self.smtp_user, self.smtp_password)
                    
                    # Send email
                    server.send_message(msg)
                
                logger.info(f"Pet story email sent successfully to {to_email}")
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"SMTP authentication failed: {str(e)}")
                return False
            except smtplib.SMTPException as e:
                logger.error(f"SMTP error occurred: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error sending email: {str(e)}", exc_info=True)
                return False
            
        except Exception as e:
            logger.error(f"Error sending pet story email to {to_email}: {str(e)}", exc_info=True)
            return False

