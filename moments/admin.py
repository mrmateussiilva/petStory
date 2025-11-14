from django.contrib import admin
from .models import Moment


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ['title', 'pet', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'text', 'pet__name']
    readonly_fields = ['created_at', 'updated_at']

