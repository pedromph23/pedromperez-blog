from django.contrib.admin import AdminSite

class SecureAdminSite(AdminSite):
    site_header = "Código y Compás — Administración"
    site_title = "Código y Compás"
    index_title = "Panel de control"
    site_url = "/"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

secure_admin_site = SecureAdminSite(name="secure_admin")
