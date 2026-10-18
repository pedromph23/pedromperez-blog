from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F
from .models import Publicacion, Categoria, Etiqueta

def post_list(request):
    qs = Publicacion.objects.filter(publicado=True).select_related("categoria").prefetch_related("etiquetas")
    categoria_slug = request.GET.get("categoria")
    etiqueta_slug = request.GET.get("etiqueta")
    if categoria_slug: qs = qs.filter(categoria__slug=categoria_slug)
    if etiqueta_slug: qs = qs.filter(etiquetas__slug=etiqueta_slug)
    paginator = Paginator(qs, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {
        "page_obj": page, 
        "categorias": Categoria.objects.all(),
        "etiquetas": Etiqueta.objects.all(), 
        "current_category": categoria_slug, 
        "current_tag": etiqueta_slug,
    })

def post_detail(request, slug):
    publicacion = get_object_or_404(Publicacion.objects.select_related("categoria").prefetch_related("etiquetas"), slug=slug, publicado=True)
    Publicacion.objects.filter(pk=publicacion.pk).update(visitas=F("visitas") + 1)
    related = Publicacion.objects.filter(publicado=True, categoria=publicacion.categoria).exclude(pk=publicacion.pk)[:3]
    return render(request, "blog/detail.html", {"publicacion": publicacion, "relacionados": related})

def category_detail(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    publicaciones = Publicacion.objects.filter(publicado=True, categoria=categoria)
    return render(request, "blog/list.html", {
        "page_obj": publicaciones, 
        "categorias": Categoria.objects.all(),
        "etiquetas": Etiqueta.objects.all(), 
        "current_category": categoria.slug, 
        "category": categoria,
    })
