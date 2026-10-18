from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Publicacion, Categoria
from projects.models import Proyecto

class StaticViewSitemap(Sitemap):
    priority = 0.8; changefreq = "monthly"
    def items(self): return ["core:home", "blog:list", "proyectos:list", "core:about", "core:contact"]
    def location(self, item): return reverse(item)

class PublicacionSitemap(Sitemap):
    priority = 0.9; changefreq = "weekly"
    def items(self): return Publicacion.objects.filter(publicado=True).order_by("-fecha_publicacion")
    def lastmod(self, obj): return obj.actualizado_el

class CategoriaSitemap(Sitemap):
    priority = 0.6; changefreq = "weekly"
    def items(self): return Categoria.objects.all()

class ProyectoSitemap(Sitemap):
    priority = 0.7; changefreq = "monthly"
    def items(self): return Proyecto.objects.all()
