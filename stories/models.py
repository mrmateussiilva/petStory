from django.db import models
from pets.models import Pet


class Story(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='story')
    generated_text = models.TextField(verbose_name='História Gerada')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_premium = models.BooleanField(default=False, verbose_name='Versão Premium')
    
    class Meta:
        verbose_name = 'História'
        verbose_name_plural = 'Histórias'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"História de {self.pet.name}"

