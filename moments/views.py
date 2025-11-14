from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pets.models import Pet
from .models import Moment
from .forms import MomentForm


def moments_add(request, slug):
    """Adicionar momentos ao pet"""
    pet = get_object_or_404(Pet, slug=slug)
    moments = pet.moments.all()
    
    # Definir limite baseado no plano
    max_moments = 10 if pet.plan == 'premium' else 2
    min_moments = 2  # Mínimo para gerar história
    
    # Verificar se atingiu o limite
    if len(moments) >= max_moments:
        plan_text = "Premium (10 momentos)" if pet.plan == 'premium' else "FREE (2 momentos)"
        messages.warning(request, f'Você já adicionou o máximo de {max_moments} momentos do plano {plan_text}!')
        return redirect('pets:pet_detail', slug=slug)
    
    if request.method == 'POST':
        form = MomentForm(request.POST, request.FILES)
        if form.is_valid():
            # Verificar novamente o limite antes de salvar (caso tenha mudado)
            current_moments = pet.moments.count()
            if current_moments >= max_moments:
                plan_text = "Premium (10 momentos)" if pet.plan == 'premium' else "FREE (2 momentos)"
                messages.warning(request, f'Você já atingiu o limite máximo de {max_moments} momentos do plano {plan_text}!')
                return redirect('pets:pet_detail', slug=slug)
            
            moment = form.save(commit=False)
            moment.pet = pet
            moment.save()
            messages.success(request, 'Momento adicionado com sucesso!')
            
            # Se já tem o mínimo de momentos, pode gerar história
            if pet.moments.count() >= min_moments:
                return redirect('pets:pet_detail', slug=slug)
            else:
                return redirect('moments:add', slug=slug)
    else:
        form = MomentForm()
    
    context = {
        'pet': pet,
        'form': form,
        'moments': moments,
        'max_moments': max_moments,
        'min_moments': min_moments,
        'can_add_more': len(moments) < max_moments,
        'moments_count': len(moments),
    }
    
    return render(request, 'moments/moments_add.html', context)


def moment_delete(request, slug, moment_id):
    """Deletar momento"""
    pet = get_object_or_404(Pet, slug=slug)
    moment = get_object_or_404(Moment, id=moment_id, pet=pet)
    
    if request.method == 'POST':
        moment.delete()
        messages.success(request, 'Momento deletado com sucesso!')
        return redirect('pets:pet_detail', slug=slug)
    
    return render(request, 'moments/moment_delete.html', {'pet': pet, 'moment': moment})

