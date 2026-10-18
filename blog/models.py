from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from core.validators import validar_slug_seguro

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=120, unique=True, blank=True, validators=[validar_slug_seguro])
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self): return self.nombre
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("blog:category", kwargs={"slug": self.slug})

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ["nombre"]

    def __str__(self): return self.nombre
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200, validators=[MinLengthValidator(5)], verbose_name="Título")
    slug = models.SlugField(max_length=220, unique=True, blank=True, validators=[validar_slug_seguro])
    resumen = models.TextField(blank=True, max_length=300, verbose_name="Resumen")
    contenido = models.TextField(validators=[MinLengthValidator(50)], verbose_name="Contenido")
    imagen_portada = models.ImageField(upload_to="portadas/", blank=True, null=True, verbose_name="Imagen de Portada")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="publicaciones", verbose_name="Categoría")
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name="publicaciones", verbose_name="Etiquetas")
    autor = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="publicaciones", verbose_name="Autor")
    publicado = models.BooleanField(default=False, verbose_name="¿Está Publicado?")
    fecha_publicacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Publicación")
    tiempo_lectura = models.PositiveIntegerField(default=0, help_text="Minutos", verbose_name="Tiempo de Lectura")
    visitas = models.PositiveIntegerField(default=0, verbose_name="Visitas")
    creado_el = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    actualizado_el = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ["-fecha_publicacion", "-creado_el"]

    def __str__(self): return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.titulo)[:220]
        if self.publicado and not self.fecha_publicacion: self.fecha_publicacion = timezone.now()
        if not self.tiempo_lectura: self.tiempo_lectura = max(1, len(self.contenido.split()) // 200)
        super().save(*args, **kwargs)

    def get_absolute_url(self): return reverse("blog:detail", kwargs={"slug": self.slug})
