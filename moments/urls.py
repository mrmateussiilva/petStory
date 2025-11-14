from django.urls import path
from . import views

app_name = 'moments'

urlpatterns = [
    path('add/<slug:slug>/', views.moments_add, name='add'),
    path('delete/<slug:slug>/<int:moment_id>/', views.moment_delete, name='delete'),
]

