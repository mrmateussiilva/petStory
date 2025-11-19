"""
Utilitários para geração de PDF e marca d'água
"""
from io import BytesIO
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os


def add_watermark_to_image(image_path, is_premium=False):
    """
    Adiciona marca d'água à imagem
    Se for premium, não adiciona marca d'água
    """
    if is_premium:
        return image_path
    
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Configurar fonte (tentar usar fonte padrão)
        try:
            font_size = max(20, int(img.width / 20))
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Texto da marca d'água
        watermark_text = "Criado com PetStory — Faça o seu!"
        
        # Calcular posição (canto inferior direito)
        if font:
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(watermark_text) * 10
            text_height = 20
        
        x = img.width - text_width - 20
        y = img.height - text_height - 20
        
        # Desenhar fundo semi-transparente
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [x - 10, y - 5, x + text_width + 10, y + text_height + 5],
            fill=(0, 0, 0, 128)
        )
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Desenhar texto
        draw.text((x, y), watermark_text, fill=(255, 255, 255), font=font)
        
        # Salvar imagem com marca d'água
        watermark_path = image_path.replace('.', '_watermark.')
        img.save(watermark_path)
        
        return watermark_path
    
    except Exception as e:
        print(f"Erro ao adicionar marca d'água: {e}")
        return image_path


def generate_pdf(pet, story):
    """
    Gera PDF da história do pet
    """
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        raise ImportError("weasyprint não está instalado. Instale com: pip install weasyprint")
    
    from django.template.loader import render_to_string
    
    # Preparar contexto
    moments = pet.moments.all()
    
    # Adicionar marca d'água na foto se não for premium
    photo_path = None
    if pet.photo:
        photo_path = pet.photo.path
        if not story.is_premium:
            photo_path = add_watermark_to_image(photo_path, is_premium=False)
    
    context = {
        'pet': pet,
        'story': story,
        'moments': moments,
        'photo_path': photo_path,
    }
    
    # Renderizar HTML
    html_string = render_to_string('stories/story_pdf.html', context)
    
    # Configurar CSS
    css_string = """
    @page {
        size: A4;
        margin: 2cm;
    }
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
    }
    .watermark {
        position: fixed;
        bottom: 1cm;
        right: 1cm;
        color: rgba(0, 0, 0, 0.3);
        font-size: 10px;
        font-style: italic;
    }
    """
    
    if story.is_premium:
        css_string += ".watermark { display: none; }"
    
    # Gerar PDF
    font_config = FontConfiguration()
    base_url = str(settings.BASE_DIR) if hasattr(settings.BASE_DIR, '__str__') else settings.BASE_DIR
    html = HTML(string=html_string, base_url=base_url)
    css = CSS(string=css_string, font_config=font_config)
    
    pdf_bytes = html.write_pdf(stylesheets=[css], font_config=font_config)
    
    return pdf_bytes

