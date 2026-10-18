from django.contrib import admin
from .models import Categoria, Etiqueta, Publicacion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "publicado", "fecha_publicacion", "tiempo_lectura")
    list_filter = ("publicado", "categoria", "etiquetas")
    search_fields = ("titulo", "resumen", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
    filter_horizontal = ("etiquetas",)
    date_hierarchy = "fecha_publicacion"
