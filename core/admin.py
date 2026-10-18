from django.contrib import admin
from .models import MensajeContacto

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "asunto", "leido", "creado_el")
    list_filter = ("leido", "creado_el")
    search_fields = ("nombre", "email", "mensaje")
    readonly_fields = ("nombre", "email", "asunto", "mensaje", "creado_el")
