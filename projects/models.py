from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from core.validators import validar_tech_stack

class Proyecto(models.Model):
    nombre = models.CharField(max_length=120, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    descripcion = models.TextField(validators=[MinLengthValidator(20)], verbose_name="Descripción")
    url_github = models.URLField(blank=True, verbose_name="URL de GitHub")
    url_demo = models.URLField(blank=True, verbose_name="URL de Demo")
    tecnologias = models.JSONField(default=list, blank=True, validators=[validar_tech_stack], verbose_name="Tecnologías")
    imagen = models.ImageField(upload_to="proyectos/", blank=True, null=True, verbose_name="Imagen")
    destacado = models.BooleanField(default=False, verbose_name="¿Destacado?")
    posicion = models.PositiveIntegerField(default=0, verbose_name="Posición")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ["posicion", "nombre"]

    def __str__(self): return self.nombre
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("proyectos:detail", kwargs={"slug": self.slug})
