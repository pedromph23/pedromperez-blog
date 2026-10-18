import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_slug_seguro(value):
    """Solo minúsculas, números y guiones."""
    if not re.match(r"^[a-z0-9-]+$", value):
        raise ValidationError(_("El slug solo puede contener minúsculas, números y guiones."))

def validar_tech_stack(value):
    """Valida que tech_stack sea una lista de strings no vacíos."""
    if not isinstance(value, list) or not all(isinstance(t, str) and t.strip() for t in value):
        raise ValidationError(_("Debe ser una lista de tecnologías (texto no vacío)."))

# NOTA: validar_longitud_minima() era un closure y rompía las migraciones.
# Usaremos MinLengthValidator de Django en los modelos.
