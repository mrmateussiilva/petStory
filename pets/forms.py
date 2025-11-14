from django import forms
from .models import Pet


class PetForm(forms.ModelForm):
    PLAN_CHOICES = [
        ('free', 'Plano FREE - Grátis'),
        ('premium', 'Plano Premium - R$ 49,90'),
    ]
    
    plan = forms.ChoiceField(
        choices=PLAN_CHOICES,
        initial='free',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Escolha o Plano',
        help_text='O plano Premium remove a marca d\'água e oferece recursos exclusivos'
    )
    
    class Meta:
        model = Pet
        fields = ['name', 'species', 'birth_date', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do pet'
            }),
            'species': forms.Select(attrs={
                'class': 'form-select'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'name': 'Nome',
            'species': 'Espécie',
            'birth_date': 'Data de Nascimento',
            'photo': 'Foto Principal',
        }

