from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('generate/<slug:slug>/', views.generate_story_view, name='generate'),
    path('view/<slug:slug>/', views.story_view, name='view'),
    path('pdf/<slug:slug>/', views.download_pdf, name='pdf'),
    path('premium/success/', views.premium_success, name='premium_success'),
]

