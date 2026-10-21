import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from blog.models import Publicacion
from projects.models import Proyecto
from .forms import ContactForm

def home(request):
    publicaciones = Publicacion.objects.filter(publicado=True).select_related("categoria")[:6]
    proyectos_destacados = Proyecto.objects.filter(destacado=True)[:3]
    return render(request, "core/home.html", {"publicaciones": publicaciones, "proyectos_destacados": proyectos_destacados})

def about(request):
    return render(request, "core/about.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # 1. Guardar en la base de datos (Supabase/Local)
            form.save()
            
            # 2. Reenviar a Formspree
            try:
                requests.post(
                    "https://formspree.io/f/xyekqnne",
                    data={
                        "nombre": form.cleaned_data["nombre"],
                        "email": form.cleaned_data["email"],
                        "asunto": form.cleaned_data["asunto"],
                        "mensaje": form.cleaned_data["mensaje"],
                    },
                    headers={"Accept": "application/json"},
                    timeout=5
                )
            except Exception as e:
                print(f"⚠️ Error enviando a Formspree: {e}")
            
            # 3. Responder (AJAX o HTML normal)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": "¡Gracias! Tu mensaje ha sido enviado y guardado."})
            
            messages.success(request, "¡Gracias! Tu mensaje ha sido guardado y enviado.")
            return redirect("core:contact")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        form = ContactForm()
    
    return render(request, "core/contact.html", {"form": form})
