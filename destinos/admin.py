from django.contrib import admin

from .models import BlogEmpresa, Destino, Garantia, OfertaEmpresa, Paquete, Testimonio

@admin.register(Destino)
class DestinoAdmin(admin.ModelAdmin):
    list_display = ['pais', 'continente', 'precio_desde', 'activo', 'orden']
    list_filter = ['continente', 'activo']
    search_fields = ['pais', 'codigo_pais', 'descripcion', 'comida', 'transfers']
    readonly_fields = ['created_at']
    ordering = ['orden', 'pais']

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'destino', 'precio', 'duracion_dias', 'destacado', 'disponible', 'created_at']
    list_filter = ['destacado', 'disponible', 'destino']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['created_at']

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'viaje', 'rating', 'aprobado', 'fecha']
    list_filter = ['aprobado', 'rating', 'fecha']
    search_fields = ['nombre', 'texto', 'viaje']
    readonly_fields = ['fecha']
    ordering = ['-fecha']

@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'icono', 'orden', 'activo']
    list_filter = ['activo']
    search_fields = ['titulo', 'descripcion', 'icono']
    ordering = ['orden']


@admin.register(OfertaEmpresa)
class OfertaEmpresaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'destino', 'precio', 'duracion', 'destacada', 'status', 'created_at']
    list_filter = ['destacada', 'status', 'destino']
    search_fields = ['titulo', 'descripcion', 'destino__pais']
    readonly_fields = ['created_at']


@admin.register(BlogEmpresa)
class BlogEmpresaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'slug', 'autor', 'lectura_minutos', 'status', 'created_at']
    list_filter = ['status', 'autor']
    search_fields = ['titulo', 'slug', 'excerpt', 'contenido', 'autor']
    readonly_fields = ['created_at']
