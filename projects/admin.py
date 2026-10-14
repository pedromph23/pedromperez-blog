from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "featured", "position")
    list_filter = ("featured",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
