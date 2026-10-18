from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Publicacion, Categoria, Etiqueta

class CategoriaModelTests(TestCase):
    def test_slug_auto(self):
        cat = Categoria.objects.create(nombre="Desarrollo Web")
        self.assertEqual(cat.slug, "desarrollo-web")

    def test_slug_no_sobrescribe(self):
        cat = Categoria.objects.create(nombre="Frontend", slug="front-custom")
        self.assertEqual(cat.slug, "front-custom")

class EtiquetaModelTests(TestCase):
    def test_slug_auto(self):
        tag = Etiqueta.objects.create(nombre="Django REST")
        self.assertEqual(tag.slug, "django-rest")

class PublicacionModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test", password="testpass123")
        self.cat = Categoria.objects.create(nombre="Backend")

    def test_slug_auto(self):
        pub = Publicacion.objects.create(titulo="Mi primer post sobre Django", contenido="Contenido de prueba", autor=self.user)
        self.assertEqual(pub.slug, "mi-primer-post-sobre-django")

    def test_tiempo_lectura_auto(self):
        contenido = " ".join(["palabra"] * 400)
        pub = Publicacion.objects.create(titulo="Post largo", contenido=contenido, autor=self.user)
        self.assertEqual(pub.tiempo_lectura, 2)

    def test_fecha_publicacion_auto(self):
        pub = Publicacion.objects.create(titulo="Publicado", contenido="x"*50, publicado=True, autor=self.user)
        self.assertIsNotNone(pub.fecha_publicacion)
        self.assertLessEqual(pub.fecha_publicacion, timezone.now())

    def test_validacion_titulo_corto(self):
        pub = Publicacion(titulo="Cort", contenido="x"*50)
        with self.assertRaises(ValidationError):
            pub.full_clean()

class BlogViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="test", password="testpass123")
        self.cat = Categoria.objects.create(nombre="Backend")
        self.pub = Publicacion.objects.create(
            titulo="Publicación pública", slug="publicacion-publica",
            contenido="Contenido", publicado=True, autor=self.user, categoria=self.cat
        )

    def test_blog_list_200(self):
        r = self.client.get("/blog/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Publicación pública")

    def test_blog_detail_200(self):
        r = self.client.get(f"/blog/{self.pub.slug}/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Publicación pública")

    def test_visitas_incrementa(self):
        pub = Publicacion.objects.get(pk=self.pub.pk)
        visitas_iniciales = pub.visitas
        self.client.get(f"/blog/{pub.slug}/")
        pub.refresh_from_db()
        self.assertEqual(pub.visitas, visitas_iniciales + 1)
