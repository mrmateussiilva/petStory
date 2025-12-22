"""PDF generation service for compiling coloring book pages."""

import io
import logging
from typing import List, Optional

from fpdf import FPDF
from PIL import Image

logger = logging.getLogger(__name__)


class PDFService:
    """Service for creating PDFs from images."""

    # A4 dimensions in mm
    A4_WIDTH_MM = 210
    A4_HEIGHT_MM = 297
    MARGIN_MM = 10

    def __init__(self):
        """Initialize PDF service."""
        pass

    def create_pdf_from_images(
        self, images: List[bytes], output_path: Optional[str] = None
    ) -> bytes:
        """Create a PDF from a list of image bytes.
        
        Args:
            images: List of image bytes (PNG/JPEG)
            output_path: Optional path to save PDF. If None, returns bytes.
            
        Returns:
            PDF as bytes
        """
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        
        for idx, image_bytes in enumerate(images):
            try:
                # Load image
                img = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if necessary
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                # Calculate dimensions to fit A4 with margins
                available_width = self.A4_WIDTH_MM - (2 * self.MARGIN_MM)
                available_height = self.A4_HEIGHT_MM - (2 * self.MARGIN_MM)
                
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height
                
                # Fit image to available space maintaining aspect ratio
                if aspect_ratio > (available_width / available_height):
                    # Image is wider
                    width = available_width
                    height = available_width / aspect_ratio
                else:
                    # Image is taller
                    height = available_height
                    width = available_height * aspect_ratio
                
                # Center image
                x_offset = (self.A4_WIDTH_MM - width) / 2
                y_offset = (self.A4_HEIGHT_MM - height) / 2
                
                # Save image to temporary file for FPDF
                temp_buffer = io.BytesIO()
                img.save(temp_buffer, format="PNG")
                temp_buffer.seek(0)
                
                # Add page
                pdf.add_page()
                
                # Add image to PDF
                pdf.image(
                    temp_buffer,
                    x=x_offset,
                    y=y_offset,
                    w=width,
                    h=height,
                )
                
                logger.info(f"Added image {idx + 1}/{len(images)} to PDF")
                
            except Exception as e:
                logger.error(
                    f"Error adding image {idx + 1} to PDF: {str(e)}",
                    exc_info=True,
                )
                # Continue with next image even if one fails
                continue
        
        if output_path:
            pdf.output(output_path)
            logger.info(f"PDF saved to {output_path}")
            return b""
        else:
            # Return PDF as bytes
            # pdf.output(dest="S") returns bytes/bytearray, not a string
            pdf_output = pdf.output(dest="S")
            if isinstance(pdf_output, bytearray):
                pdf_bytes = bytes(pdf_output)
            elif isinstance(pdf_output, bytes):
                pdf_bytes = pdf_output
            else:
                # If it's a string, encode it
                pdf_bytes = pdf_output.encode("latin-1")
            logger.info(f"PDF generated ({len(pdf_bytes)} bytes)")
            return pdf_bytes
    
    def create_digital_kit(
        self,
        pet_name: str,
        pet_date: str,
        pet_story: str,
        image_path: str,
        output_dir: str = ".",
        original_photo_path: Optional[str] = None,
    ) -> str:
        """Create a digital kit PDF with 4 pages: cover, biography, coloring page, and sticker grid.
        
        Args:
            pet_name: Pet's name
            pet_date: Pet's date/birthday
            pet_story: Pet's story/biography text
            image_path: Path to the generated art image (for coloring page and stickers)
            output_dir: Directory to save the PDF
            original_photo_path: Optional path to original photo (for cover page)
            
        Returns:
            Path to the created PDF file
        """
        import os
        from datetime import datetime
        
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Page 1: Cover with title, name and centered photo
        pdf.add_page()
        pdf.set_font("Arial", "B", 24)
        pdf.cell(0, 20, "Livro do Pet", ln=1, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 15, pet_name, ln=1, align="C")
        pdf.ln(10)
        
        # Load and add photo (use original photo on cover if available, otherwise use art)
        cover_image_path = original_photo_path if original_photo_path else image_path
        try:
            img = Image.open(cover_image_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Calculate size to fit in center (max 120mm width, maintaining aspect)
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
            
            max_width = 120
            max_height = 100
            
            if aspect_ratio > (max_width / max_height):
                width = max_width
                height = max_width / aspect_ratio
            else:
                height = max_height
                width = max_height * aspect_ratio
            
            # Center image
            x = (self.A4_WIDTH_MM - width) / 2
            y = pdf.get_y() + 10
            
            # Save image to temp buffer
            temp_buffer = io.BytesIO()
            img.save(temp_buffer, format="PNG")
            temp_buffer.seek(0)
            
            pdf.image(temp_buffer, x=x, y=y, w=width, h=height)
        except Exception as e:
            logger.warning(f"Could not add image to cover: {e}")
        
        # Page 2: Biography
        pdf.add_page()
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 15, f"Quem é {pet_name}?", ln=1)
        pdf.ln(5)
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Data: {pet_date}", ln=1)
        pdf.ln(5)
        
        pdf.set_font("Arial", "", 11)
        # Use multi_cell for text wrapping
        pdf.multi_cell(0, 7, pet_story)
        
        # Page 3: Large coloring page with generated art
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 15, "Página para Colorir", ln=1, align="C")
        pdf.ln(5)
        
        try:
            img = Image.open(image_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Calculate size to fill most of the page (larger than cover)
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
            
            available_width = self.A4_WIDTH_MM - (2 * self.MARGIN_MM)
            available_height = self.A4_HEIGHT_MM - 60  # Leave space for title
            
            if aspect_ratio > (available_width / available_height):
                width = available_width
                height = available_width / aspect_ratio
            else:
                height = available_height
                width = available_height * aspect_ratio
            
            # Center image
            x = (self.A4_WIDTH_MM - width) / 2
            y = pdf.get_y() + 5
            
            temp_buffer = io.BytesIO()
            img.save(temp_buffer, format="PNG")
            temp_buffer.seek(0)
            
            pdf.image(temp_buffer, x=x, y=y, w=width, h=height)
        except Exception as e:
            logger.error(f"Error adding coloring page image: {e}")
        
        # Page 4: Sticker grid 3x3
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 15, "Adesivos", ln=1, align="C")
        pdf.ln(5)
        
        try:
            img = Image.open(image_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Grid 3x3 = 9 stickers
            # Each sticker should be about 50mm (with some spacing)
            sticker_size = 50
            spacing = 10
            start_x = (self.A4_WIDTH_MM - (3 * sticker_size + 2 * spacing)) / 2
            start_y = pdf.get_y() + 5
            
            temp_buffer = io.BytesIO()
            img.save(temp_buffer, format="PNG")
            temp_buffer.seek(0)
            
            # Draw 3x3 grid
            for row in range(3):
                for col in range(3):
                    x = start_x + col * (sticker_size + spacing)
                    y = start_y + row * (sticker_size + spacing)
                    
                    temp_buffer.seek(0)
                    pdf.image(temp_buffer, x=x, y=y, w=sticker_size, h=sticker_size)
        except Exception as e:
            logger.error(f"Error adding sticker grid: {e}")
        
        # Save PDF
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = os.path.join(output_dir, f"kit_digital_{timestamp}.pdf")
        pdf.output(pdf_filename)
        
        logger.info(f"Digital kit PDF created: {pdf_filename}")
        return pdf_filename

