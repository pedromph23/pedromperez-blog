from django.test import TestCase, Client
from .models import Proyecto

class ProyectoModelTests(TestCase):
    def test_slug_auto(self):
        p = Proyecto.objects.create(nombre="Laws Website", descripcion="Descripción de prueba")
        self.assertEqual(p.slug, "laws-website")

    def test_tecnologias_json(self):
        p = Proyecto.objects.create(nombre="Test", descripcion="Descripción de prueba", tecnologias=["Django", "Python"])
        p.refresh_from_db()
        self.assertEqual(p.tecnologias, ["Django", "Python"])

class ProyectoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.proyecto = Proyecto.objects.create(
            nombre="Laws Website", descripcion="Sitio de leyes",
            tecnologias=["Next.js", "Supabase"], destacado=True
        )

    def test_list_200(self):
        r = self.client.get("/proyectos/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Laws Website")

    def test_detail_200(self):
        r = self.client.get(f"/proyectos/{self.proyecto.slug}/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Sitio de leyes")
