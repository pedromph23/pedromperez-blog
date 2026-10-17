from django.test import TestCase, Client


class CoreViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_200(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_about_200(self):
        r = self.client.get("/sobre-mi/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Pedro Manuel Pérez Herrera")

    def test_contact_get_200(self):
        r = self.client.get("/contacto/")
        self.assertEqual(r.status_code, 200)

    def test_contact_post_valido(self):
        r = self.client.post("/contacto/", {
            "name": "Juan",
            "email": "juan@example.com",
            "subject": "Hola",
            "body": "Mensaje de prueba",
        })
        self.assertEqual(r.status_code, 302)  # redirect tras éxito

    def test_contact_post_invalido(self):
        r = self.client.post("/contacto/", {
            "name": "",
            "email": "",
            "body": "",
        })
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "obligatorios")


class SEOTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sitemap_200(self):
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/xml")

    def test_robots_200(self):
        r = self.client.get("/robots.txt")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "User-agent")
        self.assertContains(r, "Sitemap")

    def test_rss_200(self):
        r = self.client.get("/rss.xml")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Código y Compás")

    def test_health_200(self):
        r = self.client.get("/health/")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["database"], "ok")

    def test_home_tiene_og_tags(self):
        r = self.client.get("/")
        self.assertContains(r, 'property="og:title"')
        self.assertContains(r, 'property="og:image"')
        self.assertContains(r, 'name="twitter:card"')

    def test_home_tiene_jsonld(self):
        r = self.client.get("/")
        self.assertContains(r, "application/ld+json")
        self.assertContains(r, '"@type": "Person"')
        self.assertContains(r, '"@type": "WebSite"')

# =============================================================
# TESTS: Validaciones, Formularios, Admin Seguro
# =============================================================
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from core.validators import validar_slug_seguro, validar_longitud_minima, validar_tech_stack
from core.forms import ContactForm
from blog.models import Post

class ValidatorTests(TestCase):
    def test_slug_valido(self):
        validar_slug_seguro("mi-post-2026")

    def test_slug_invalido_mayusculas(self):
        with self.assertRaises(ValidationError):
            validar_slug_seguro("Mi-Post")

    def test_longitud_minima(self):
        val = validar_longitud_minima(5)
        with self.assertRaises(ValidationError):
            val("hola")
        val("hola mundo")

    def test_tech_stack_invalido(self):
        with self.assertRaises(ValidationError):
            validar_tech_stack(["Django", ""])
        with self.assertRaises(ValidationError):
            validar_tech_stack("Django")

class ContactFormTests(TestCase):
    def test_form_valido(self):
        form = ContactForm(data={
            "name": "Juan",
            "email": "juan@test.com",
            "subject": "Hola",
            "body": "Este es un mensaje de prueba válido."
        })
        self.assertTrue(form.is_valid())

    def test_form_invalido_por_enlaces(self):
        form = ContactForm(data={
            "name": "Juan",
            "email": "juan@test.com",
            "subject": "Hola",
            "body": "Mira esto http://spam.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("body", form.errors)

    def test_form_invalido_por_longitud(self):
        form = ContactForm(data={
            "name": "J",
            "email": "juan@test.com",
            "body": "Corto"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("body", form.errors)

class SecureAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.admin = self.User.objects.create_superuser("admin", "a@a.com", "pass")
        self.user = self.User.objects.create_user("user", "u@u.com", "pass")

    def test_admin_url_es_custom(self):
        r = self.client.get("/admin/")
        self.assertEqual(r.status_code, 404)

    def test_admin_url_requiere_login(self):
        r = self.client.get("/gestion-interna/")
        self.assertEqual(r.status_code, 302)

    def test_admin_url_rechaza_no_superuser(self):
        self.client.force_login(self.user)
        r = self.client.get("/gestion-interna/")
        self.assertEqual(r.status_code, 302)

    def test_admin_url_acepta_superuser(self):
        self.client.force_login(self.admin)
        r = self.client.get("/gestion-interna/")
        self.assertEqual(r.status_code, 200)

# =============================================================
# TESTS: Verificación de la UI del Admin Personalizado
# =============================================================
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminUITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.admin_user = self.User.objects.create_superuser(
            username='admin_ui_test',
            email='admin@ui.test',
            password='password123'
        )
        self.client.force_login(self.admin_user)

    def test_admin_loads_custom_assets(self):
        """Verifica que el CSS y JS personalizados se cargan en el admin."""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin/css/admin-theme.css')
        self.assertContains(response, 'gsap.min.js')
        self.assertContains(response, 'admin/js/admin-animations.js')

    def test_admin_smoke_test(self):
        """Prueba de humo: verifica que las páginas principales del admin devuelven 200."""
        urls = [
            reverse('admin:index'),
            reverse('admin:blog_post_changelist'),
            reverse('admin:blog_post_add'),
            reverse('admin:auth_user_changelist'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200, f"La URL {url} falló con {response.status_code}")
