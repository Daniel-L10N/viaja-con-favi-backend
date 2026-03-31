from django.contrib import admin
from .models import Destino, Paquete, Testimonio, Garantia

@admin.register(Destino)
class DestinoAdmin(admin.ModelAdmin):
    list_display = ['pais', 'continente', 'precio_desde', 'activo', 'orden']
    list_filter = ['continente', 'activo']
    search_fields = ['pais']
    ordering = ['orden', 'pais']

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'destino', 'precio', 'duracion_dias', 'destacado', 'disponible']
    list_filter = ['destacado', 'disponible', 'destino']
    search_fields = ['titulo', 'descripcion']

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'viaje', 'rating', 'aprobado', 'fecha']
    list_filter = ['aprobado', 'rating', 'fecha']
    search_fields = ['nombre', 'texto', 'viaje']
    ordering = ['-fecha']

@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'icono', 'orden', 'activo']
    list_filter = ['activo']
    ordering = ['orden']