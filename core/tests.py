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
