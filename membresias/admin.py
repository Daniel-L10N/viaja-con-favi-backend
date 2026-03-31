from django.contrib import admin
from .models import Plan, Membresia, Referral

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'subtitulo', 'precio', 'mensualidad', 'puntos_inicio', 'activo', 'orden']
    list_filter = ['activo', 'nombre']
    ordering = ['orden']

@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'plan', 'estado', 'fecha_inicio', 'fecha_renovacion', 'created_at']
    list_filter = ['estado', 'plan', 'created_at']
    search_fields = ['usuario__email', 'usuario__first_name', 'usuario__last_name']
    ordering = ['-created_at']

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referidor', 'referido', 'membresia', 'membresia_activa', 'fecha']
    list_filter = ['membresia_activa', 'fecha']
    search_fields = ['referidor__email', 'referido__email']
    ordering = ['-fecha']