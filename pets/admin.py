from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'species', 'plan', 'birth_date', 'created_at']
    list_filter = ['species', 'plan', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['slug', 'created_at', 'updated_at']

