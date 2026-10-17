import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_slug_seguro(value):
    """Solo minúsculas, números y guiones."""
    if not re.match(r"^[a-z0-9-]+$", value):
        raise ValidationError(_("El slug solo puede contener minúsculas, números y guiones."))

def validar_longitud_minima(min_length):
    """Valida la longitud mínima ignorando espacios."""
    def validator(value):
        if len(value.strip()) < min_length:
            raise ValidationError(
                _("Este campo debe tener al menos %(min)s caracteres.") % {"min": min_length}
            )
    return validator

def validar_tech_stack(value):
    """Valida que tech_stack sea una lista de strings no vacíos."""
    if not isinstance(value, list) or not all(isinstance(t, str) and t.strip() for t in value):
        raise ValidationError(_("Debe ser una lista de tecnologías (texto no vacío)."))
