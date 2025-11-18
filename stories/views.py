from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from pets.models import Pet
from .models import Story
from .services import generate_story
from .utils import generate_pdf


def generate_story_view(request, slug):
    """Gerar história com IA"""
    pet = get_object_or_404(Pet, slug=slug)
    moments = pet.moments.all()
    
    # Definir limites baseado no plano
    max_moments = 10 if pet.plan == 'premium' else 2
    min_moments = 2
    
    # Validar quantidade de momentos
    if len(moments) < min_moments:
        messages.error(request, f'Você precisa adicionar pelo menos {min_moments} momentos antes de gerar a história!')
        return redirect('moments:add', slug=slug)
    
    if len(moments) > max_moments:
        plan_text = "Premium (máximo 10)" if pet.plan == 'premium' else "FREE (máximo 2)"
        messages.error(request, f'Você excedeu o limite do plano {plan_text}!')
        return redirect('pets:pet_detail', slug=slug)
    
    # Verificar se já existe história
    if hasattr(pet, 'story'):
        messages.info(request, 'Este pet já possui uma história gerada!')
        return redirect('stories:view', slug=slug)
    
    # Gerar história
    try:
        story_text = generate_story(pet, moments)
        
        # Determinar se é premium baseado no plano do pet
        is_premium = pet.plan == 'premium'
        
        # Criar ou atualizar história
        story, created = Story.objects.get_or_create(
            pet=pet,
            defaults={
                'generated_text': story_text,
                'is_premium': is_premium
            }
        )
        
        if not created:
            story.generated_text = story_text
            story.is_premium = is_premium
            story.save()
        
        messages.success(request, 'História gerada com sucesso!')
        return redirect('stories:view', slug=slug)
    
    except Exception as e:
        messages.error(request, f'Erro ao gerar história: {str(e)}')
        return redirect('pets:pet_detail', slug=slug)


def story_view(request, slug):
    """Visualizar história gerada"""
    pet = get_object_or_404(Pet, slug=slug)
    
    if not hasattr(pet, 'story'):
        messages.warning(request, 'Você precisa gerar a história primeiro!')
        return redirect('pets:pet_detail', slug=slug)
    
    story = pet.story
    moments = pet.moments.all()
    
    context = {
        'pet': pet,
        'story': story,
        'moments': moments,
    }
    
    return render(request, 'story/result.html', context)


def download_pdf(request, slug):
    """Baixar PDF da história"""
    pet = get_object_or_404(Pet, slug=slug)
    
    if not hasattr(pet, 'story'):
        messages.error(request, 'História não encontrada!')
        return redirect('pets:pet_detail', slug=slug)
    
    story = pet.story
    
    try:
        pdf_file = generate_pdf(pet, story)
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="historia-{pet.slug}.pdf"'
        return response
    
    except Exception as e:
        messages.error(request, f'Erro ao gerar PDF: {str(e)}')
        return redirect('stories:view', slug=slug)


def premium_success(request):
    """Página de sucesso após compra premium (placeholder)"""
    return render(request, 'stories/premium_success.html')

