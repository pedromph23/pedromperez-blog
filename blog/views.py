from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F
from .models import Post, Category, Tag


def post_list(request):
    qs = Post.objects.filter(published=True).select_related("category").prefetch_related("tags")

    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if tag_slug:
        qs = qs.filter(tags__slug=tag_slug)

    paginator = Paginator(qs, 9)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "blog/list.html", {
        "page_obj": page,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "current_category": category_slug,
        "current_tag": tag_slug,
    })


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("category").prefetch_related("tags"),
        slug=slug, published=True,
    )
    Post.objects.filter(pk=post.pk).update(views=F("views") + 1)

    related = Post.objects.filter(
        published=True, category=post.category
    ).exclude(pk=post.pk)[:3]

    return render(request, "blog/detail.html", {"post": post, "related": related})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(published=True, category=category)
    return render(request, "blog/list.html", {
        "page_obj": posts,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "current_category": category.slug,
        "category": category,
    })
