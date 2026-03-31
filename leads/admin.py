from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'plan_interes', 'estado', 'created_at']
    list_filter = ['estado', 'plan_interes', 'origen', 'created_at']
    search_fields = ['nombre', 'email', 'telefono']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']