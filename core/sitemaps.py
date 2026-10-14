from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post, Category
from projects.models import Project


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ["core:home", "blog:list", "projects:list", "core:about", "core:contact"]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Post.objects.filter(published=True).order_by("-published_at")

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Category.objects.all()


class ProjectSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        # Project no tiene updated_at; usamos el más reciente de los posts
        return None
