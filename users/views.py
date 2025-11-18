from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def landing(request):
    """Página inicial/landing page"""
    return render(request, 'landing/index.html')


def register_view(request):
    """View para registro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('pets:dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            login(request, user)
            return redirect('pets:dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """View para login"""
    if request.user.is_authenticated:
        return redirect('pets:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Bem-vindo, {username}!')
                return redirect('pets:dashboard')
            else:
                messages.error(request, 'Usuário ou senha inválidos')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

