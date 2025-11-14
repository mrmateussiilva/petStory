from django import forms
from .models import Moment


class MomentForm(forms.ModelForm):
    class Meta:
        model = Moment
        fields = ['title', 'text', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do momento'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva este momento especial...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Título',
            'text': 'Texto',
            'image': 'Foto (opcional)',
        }

