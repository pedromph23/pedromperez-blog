import re
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags
from .models import MensajeContacto

class ContactForm(forms.ModelForm):
    # Campo Honeypot: los humanos no lo ven, los bots lo rellenan
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="No llenar")

    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
            'email': forms.EmailInput(attrs={'placeholder': 'tu@email.com', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
            'asunto': forms.TextInput(attrs={'placeholder': 'Asunto', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
            'mensaje': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Mensaje...', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
        }

    def clean_honeypot(self):
        """Si el bot llena el campo oculto, bloqueamos el envío."""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError(_("Actividad sospechosa detectada (Bot)."))
        return honeypot

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        # Eliminar etiquetas HTML
        nombre = strip_tags(nombre).strip()
        # Verificar longitud mínima y máxima
        if len(nombre) < 2 or len(nombre) > 100:
            raise forms.ValidationError(_("El nombre debe tener entre 2 y 100 caracteres."))
        # Solo permitir letras, espacios, acentos, guiones y apóstrofes
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\'\-]+$", nombre):
            raise forms.ValidationError(_("El nombre contiene caracteres no permitidos."))
        return nombre

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        # Prevenir inyección de cabeceras (CRLF)
        if '\r' in email or '\n' in email:
            raise forms.ValidationError(_("El correo electrónico contiene caracteres no válidos."))
        return email

    def clean_asunto(self):
        asunto = self.cleaned_data.get('asunto', '')
        asunto = strip_tags(asunto).strip()
        # Prevenir inyección de cabeceras (CRLF)
        if '\r' in asunto or '\n' in asunto:
            raise forms.ValidationError(_("El asunto contiene caracteres no válidos."))
        if len(asunto) > 200:
            raise forms.ValidationError(_("El asunto no puede superar los 200 caracteres."))
        return asunto

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '')
        mensaje = strip_tags(mensaje).strip()
        
        if len(mensaje) < 10:
            raise forms.ValidationError(_("El mensaje es demasiado corto (mínimo 10 caracteres)."))
        if len(mensaje) > 2000:
            raise forms.ValidationError(_("El mensaje es demasiado largo (máximo 2000 caracteres)."))
            
        # Validación anti-spam: bloquear enlaces
        if "http://" in mensaje or "https://" in mensaje or "www." in mensaje:
            raise forms.ValidationError(_("El mensaje no puede contener enlaces (anti-spam)."))
            
        # Validación anti-spam: bloquear exceso de mayúsculas
        if sum(1 for c in mensaje if c.isupper()) > len(mensaje) * 0.7:
            raise forms.ValidationError(_("El mensaje contiene demasiadas mayúsculas (sospechoso de spam)."))

        return mensaje
