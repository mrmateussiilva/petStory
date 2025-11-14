from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.pet_create, name='pet_create'),
    path('<slug:slug>/', views.pet_detail, name='pet_detail'),
    path('<slug:slug>/delete/', views.pet_delete, name='pet_delete'),
    path('<slug:slug>/pdf/', views.download_pdf, name='pdf'),
    path('public/<slug:slug>/', views.public_pet, name='public_pet'),
]

