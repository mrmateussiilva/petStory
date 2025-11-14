from django.db import models
from pets.models import Pet
from PIL import Image


class Moment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='moments')
    title = models.CharField(max_length=200, verbose_name='Título')
    text = models.TextField(verbose_name='Texto')
    image = models.ImageField(upload_to='moments/images/', blank=True, null=True, verbose_name='Foto')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Momento'
        verbose_name_plural = 'Momentos'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.title} - {self.pet.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionar imagem se necessário
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 600 or img.width > 600:
                    output_size = (600, 600)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                    img.save(self.image.path)
            except Exception as e:
                print(f"Erro ao redimensionar imagem: {e}")

