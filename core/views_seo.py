from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from django.urls import reverse
from blog.models import Publicacion
from django.utils import timezone


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /health/",
        "",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def rss_feed(request):
    posts = Publicacion.objects.filter(publicado=True).select_related("category").order_by("-published_at")[:20]
    site_url = request.build_absolute_uri("/").rstrip("/")

    items = []
    for post in posts:
        pub_date = post.fecha_publicacion.strftime("%a, %d %b %Y %H:%M:%S +0000") if post.fecha_publicacion else ""
        items.append(f"""
    <item>
      <title><![CDATA[{post.titulo}]]></title>
      <link>{site_url}{post.get_absolute_url()}</link>
      <guid isPermaLink="true">{site_url}{post.get_absolute_url()}</guid>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[{post.resumen}]]></description>
    </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Código y Compás</title>
    <link>{site_url}</link>
    <description>Blog de Pedro M. Pérez H. — Full Stack Developer</description>
    <language>es-ve</language>
    <lastBuildDate>{timezone.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
    <atom:link href="{site_url}/rss.xml" rel="self" type="application/rss+xml" />
    {''.join(items)}
  </channel>
</rss>"""
    return HttpResponse(rss, content_type="application/rss+xml; charset=utf-8")


def health(request):
    from django.db import connection
    from django.http import JsonResponse

    db_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        db_ok = False

    return JsonResponse({
        "status": "ok" if db_ok else "degraded",
        "django": "ok",
        "database": "ok" if db_ok else "error",
        "version": "1.0.0",
    })
