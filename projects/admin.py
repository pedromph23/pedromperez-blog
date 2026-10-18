from django.contrib import admin
from .models import Proyecto

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "destacado", "posicion")
    list_filter = ("destacado",)
    prepopulated_fields = {"slug": ("nombre",)}
