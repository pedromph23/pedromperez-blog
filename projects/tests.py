from django.test import TestCase, Client
from .models import Project


class ProjectModelTests(TestCase):
    def test_slug_auto(self):
        p = Project.objects.create(name="Laws Website", description="x")
        self.assertEqual(p.slug, "laws-website")

    def test_tech_stack_json(self):
        p = Project.objects.create(
            name="Test", description="x",
            tech_stack=["Django", "Python"],
        )
        p.refresh_from_db()
        self.assertEqual(p.tech_stack, ["Django", "Python"])

    def test_ordering_por_position(self):
        p1 = Project.objects.create(name="A", description="x", position=2)
        p2 = Project.objects.create(name="B", description="x", position=1)
        projects = list(Project.objects.all())
        self.assertEqual(projects[0].pk, p2.pk)
        self.assertEqual(projects[1].pk, p1.pk)


class ProjectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            name="Laws Website", description="Sitio de leyes",
            tech_stack=["Next.js", "Supabase"], featured=True,
        )

    def test_list_200(self):
        r = self.client.get("/proyectos/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Laws Website")

    def test_detail_200(self):
        r = self.client.get(f"/proyectos/{self.project.slug}/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Sitio de leyes")

    def test_detail_404(self):
        r = self.client.get("/proyectos/no-existe/")
        self.assertEqual(r.status_code, 404)
