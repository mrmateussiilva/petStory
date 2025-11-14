from django.contrib import admin
from .models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['pet', 'is_premium', 'created_at']
    list_filter = ['is_premium', 'created_at']
    search_fields = ['pet__name']
    readonly_fields = ['created_at', 'updated_at']

