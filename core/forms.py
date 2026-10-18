from django import forms
from django.utils.translation import gettext_lazy as _
from .models import MensajeContacto

class ContactForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
            'email': forms.EmailInput(attrs={'placeholder': 'tu@email.com', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
            'asunto': forms.TextInput(attrs={'placeholder': 'Asunto', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
            'mensaje': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Mensaje...', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
        }

    def clean_mensaje(self):
        mensaje = self.cleaned_data["mensaje"]
        if "http://" in mensaje or "https://" in mensaje:
            raise forms.ValidationError(_("El mensaje no puede contener enlaces (anti-spam)."))
        return mensaje
