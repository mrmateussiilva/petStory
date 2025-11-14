from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404, HttpResponse
from .models import Pet
from .forms import PetForm
from stories.utils import generate_pdf


def dashboard(request):
    """Dashboard com lista de pets"""
    # Se usuário autenticado, mostrar apenas seus pets
    if request.user.is_authenticated:
        pets = Pet.objects.filter(user=request.user)
    else:
        # Se não autenticado, mostrar pets criados na sessão atual
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        # Buscar pets sem usuário (criados sem login)
        pets = Pet.objects.filter(user__isnull=True)
    
    return render(request, 'pets/dashboard.html', {'pets': pets})


def pet_create(request):
    """Criar novo pet"""
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            # Se usuário autenticado, associar ao usuário
            if request.user.is_authenticated:
                pet.user = request.user
            else:
                pet.user = None
            # Salvar o plano escolhido
            pet.plan = form.cleaned_data.get('plan', 'free')
            pet.save()
            messages.success(request, f'Pet {pet.name} criado com sucesso!')
            return redirect('pets:pet_detail', slug=pet.slug)
    else:
        form = PetForm()
    
    return render(request, 'pets/pet_create.html', {'form': form})


def pet_detail(request, slug):
    """Detalhes do pet"""
    # Permitir acesso a qualquer pet (público)
    pet = get_object_or_404(Pet, slug=slug)
    moments = pet.moments.all()
    story = getattr(pet, 'story', None)
    
    # Definir limites baseado no plano
    max_moments = 10 if pet.plan == 'premium' else 2
    min_moments = 2
    
    context = {
        'pet': pet,
        'moments': moments,
        'story': story,
        'max_moments': max_moments,
        'min_moments': min_moments,
        'can_generate_story': len(moments) >= min_moments and len(moments) <= max_moments and story is None,
        'can_add_more': len(moments) < max_moments,
    }
    
    return render(request, 'pets/pet_detail.html', context)


def pet_delete(request, slug):
    """Deletar pet"""
    pet = get_object_or_404(Pet, slug=slug)
    
    # Verificar se é o dono (se tiver usuário) ou se não tem usuário (público)
    if pet.user and pet.user != request.user:
        messages.error(request, 'Você não tem permissão para deletar este pet!')
        return redirect('pets:pet_detail', slug=slug)
    
    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()
        messages.success(request, f'Pet {pet_name} deletado com sucesso!')
        return redirect('pets:dashboard')
    
    return render(request, 'pets/pet_delete.html', {'pet': pet})


def public_pet(request, slug):
    """Página pública do pet"""
    pet = get_object_or_404(Pet, slug=slug)
    moments = pet.moments.all()
    story = getattr(pet, 'story', None)
    
    context = {
        'pet': pet,
        'moments': moments,
        'story': story,
    }
    
    return render(request, 'pets/public_pet.html', context)


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
        return redirect('pets:pet_detail', slug=slug)

