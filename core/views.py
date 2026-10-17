from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from blog.models import Post
from projects.models import Project


def home(request):
    posts = Post.objects.filter(published=True).select_related("category")[:6]
    featured = Project.objects.filter(featured=True)[:3]
    return render(request, "core/home.html", {"posts": posts, "featured": featured})


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        body = request.POST.get("body", "").strip()

        if not (name and email and body):
            messages.error(request, "Todos los campos son obligatorios.")
        else:
            # Por ahora solo logueamos. Cuando conectes SMTP lo envías.
            print(f"[CONTACTO] {name} <{email}> — {subject}\n{body}")
            messages.success(request, "¡Gracias! Tu mensaje fue recibido.")
            return redirect("core:contact")

    return render(request, "core/contact.html")
