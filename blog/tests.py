from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Post, Category, Tag


class CategoryModelTests(TestCase):
    def test_slug_auto(self):
        cat = Category.objects.create(name="Desarrollo Web")
        self.assertEqual(cat.slug, "desarrollo-web")

    def test_slug_no_sobrescribe(self):
        cat = Category.objects.create(name="Frontend", slug="front-custom")
        self.assertEqual(cat.slug, "front-custom")

    def test_str(self):
        cat = Category.objects.create(name="Backend")
        self.assertEqual(str(cat), "Backend")


class TagModelTests(TestCase):
    def test_slug_auto(self):
        tag = Tag.objects.create(name="Django REST")
        self.assertEqual(tag.slug, "django-rest")


class PostModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="testpass123"
        )
        self.cat = Category.objects.create(name="Backend")

    def test_slug_auto(self):
        post = Post.objects.create(
            title="Mi primer post sobre Django",
            content="Contenido de prueba",
            author=self.user,
        )
        self.assertEqual(post.slug, "mi-primer-post-sobre-django")

    def test_reading_time_auto(self):
        # 400 palabras → ~2 min
        content = " ".join(["palabra"] * 400)
        post = Post.objects.create(
            title="Post largo", content=content, author=self.user,
        )
        self.assertEqual(post.reading_time, 2)

    def test_published_at_auto(self):
        post = Post.objects.create(
            title="Publicado", content="x", published=True, author=self.user,
        )
        self.assertIsNotNone(post.published_at)
        self.assertLessEqual(post.published_at, timezone.now())

    def test_published_at_no_sobrescribe(self):
        fecha = timezone.now() - timezone.timedelta(days=30)
        post = Post.objects.create(
            title="Viejo", content="x", published=True,
            published_at=fecha, author=self.user,
        )
        self.assertEqual(post.published_at, fecha)

    def test_get_absolute_url(self):
        post = Post.objects.create(
            title="Test URL", content="x", author=self.user,
        )
        self.assertIn("/blog/test-url/", post.get_absolute_url())


class BlogViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test", password="testpass123"
        )
        self.cat = Category.objects.create(name="Backend")
        self.post = Post.objects.create(
            title="Post público", slug="post-publico",
            content="Contenido", published=True,
            author=self.user, category=self.cat,
        )

    def test_blog_list_200(self):
        r = self.client.get("/blog/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Post público")

    def test_blog_detail_200(self):
        r = self.client.get(f"/blog/{self.post.slug}/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Post público")

    def test_blog_detail_404_slug_inexistente(self):
        r = self.client.get("/blog/no-existe/")
        self.assertEqual(r.status_code, 404)

    def test_blog_detail_no_muestra_borradores(self):
        post_borrador = Post.objects.create(
            title="Borrador", slug="borrador",
            content="x", published=False, author=self.user,
        )
        r = self.client.get(f"/blog/{post_borrador.slug}/")
        self.assertEqual(r.status_code, 404)

    def test_blog_list_filtro_categoria(self):
        otra_cat = Category.objects.create(name="Frontend")
        post_otro = Post.objects.create(
            title="Post frontend", slug="post-frontend",
            content="x", published=True, author=self.user, category=otra_cat,
        )
        r = self.client.get(f"/blog/?category={otra_cat.slug}")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Post frontend")
        self.assertNotContains(r, "Post público")

    def test_views_incrementa(self):
        post = Post.objects.get(pk=self.post.pk)
        views_iniciales = post.views
        self.client.get(f"/blog/{post.slug}/")
        post.refresh_from_db()
        self.assertEqual(post.views, views_iniciales + 1)
