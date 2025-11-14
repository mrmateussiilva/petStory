from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
import os


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Cachorro'),
        ('cat', 'Gato'),
        ('bird', 'Pássaro'),
        ('rabbit', 'Coelho'),
        ('other', 'Outro'),
    ]
    
    PLAN_CHOICES = [
        ('free', 'FREE'),
        ('premium', 'Premium'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Nome')
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES, verbose_name='Espécie')
    birth_date = models.DateField(verbose_name='Data de Nascimento', null=True, blank=True)
    photo = models.ImageField(upload_to='pets/photos/', verbose_name='Foto Principal')
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='free', verbose_name='Plano')
    slug = models.SlugField(unique=True, max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['-created_at']
    
    def __str__(self):
        username = self.user.username if self.user else "Anônimo"
        return f"{self.name} ({username})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Pet.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        super().save(*args, **kwargs)
        
        # Redimensionar imagem se necessário
        if self.photo:
            try:
                img = Image.open(self.photo.path)
                if img.height > 800 or img.width > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                    img.save(self.photo.path)
            except Exception as e:
                print(f"Erro ao redimensionar imagem: {e}")

