from django.urls import path
from . import views

# Sem app_name para evitar conflito com pets.urls
urlpatterns = [
    path('<slug:slug>/', views.public_pet, name='public_pet'),
]

