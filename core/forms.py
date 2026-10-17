from django import forms
from django.utils.translation import gettext_lazy as _
from core.validators import validar_longitud_minima

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        validators=[validar_longitud_minima(2)],
        label=_("Nombre"),
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'})
    )
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={'placeholder': 'tu@email.com', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'})
    )
    subject = forms.CharField(
        max_length=200,
        required=False,
        label=_("Asunto"),
        widget=forms.TextInput(attrs={'placeholder': 'Asunto', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Mensaje...', 'class': 'w-full rounded-md border border-slate-700 bg-slate-900/40 px-4 py-3 text-sm focus:border-emerald-400 focus:outline-none'}),
        validators=[validar_longitud_minima(10)],
        label=_("Mensaje"),
    )

    def clean_body(self):
        body = self.cleaned_data["body"]
        if "http://" in body or "https://" in body:
            raise forms.ValidationError(_("El mensaje no puede contener enlaces."))
        return body
