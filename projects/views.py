from django.shortcuts import render, get_object_or_404
from .models import Proyecto

def project_list(request):
    proyectos = Proyecto.objects.all()
    return render(request, "projects/list.html", {"proyectos": proyectos})

def project_detail(request, slug):
    proyecto = get_object_or_404(Proyecto, slug=slug)
    return render(request, "projects/detail.html", {"proyecto": proyecto})
