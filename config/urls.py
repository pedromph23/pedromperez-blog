from core.admin_site import secure_admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import StaticViewSitemap, PostSitemap, CategorySitemap, ProjectSitemap
from core.views_seo import robots_txt, rss_feed, health

sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
    "categories": CategorySitemap,
    "projects": ProjectSitemap,
}

urlpatterns = [
    path("gestion-interna/", secure_admin_site.urls),
    path("", include("core.urls")),
    path("blog/", include("blog.urls")),
    path("proyectos/", include("projects.urls")),

    # SEO
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("rss.xml", rss_feed, name="rss_feed"),
    path("health/", health, name="health"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
