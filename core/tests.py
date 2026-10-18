from django.test import TestCase, Client
from core.models import MensajeContacto
from core.forms import ContactForm
from core.validators import validar_slug_seguro, validar_tech_stack
from django.core.exceptions import ValidationError

class ValidatorTests(TestCase):
    def test_slug_valido(self):
        validar_slug_seguro("mi-post-2026")

    def test_slug_invalido_mayusculas(self):
        with self.assertRaises(ValidationError):
            validar_slug_seguro("Mi-Post")

    def test_tech_stack_invalido(self):
        with self.assertRaises(ValidationError):
            validar_tech_stack(["Django", ""])

class ContactFormTests(TestCase):
    def test_form_valido(self):
        form = ContactForm(data={"nombre": "Juan", "email": "juan@test.com", "asunto": "Hola", "mensaje": "Este es un mensaje válido."})
        self.assertTrue(form.is_valid())

    def test_form_invalido_por_enlaces(self):
        form = ContactForm(data={"nombre": "Juan", "email": "juan@test.com", "asunto": "Hola", "mensaje": "Mira esto http://spam.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("mensaje", form.errors)

class ContactViewTests(TestCase):
    def test_contact_post_valido_guarda_en_db(self):
        r = self.client.post("/contacto/", {"nombre": "Juan", "email": "juan@test.com", "asunto": "Hola", "mensaje": "Mensaje de prueba"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(MensajeContacto.objects.count(), 1)
        self.assertEqual(MensajeContacto.objects.first().nombre, "Juan")

class SEOTests(TestCase):
    def test_sitemap_200(self):
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)
    def test_health_200(self):
        self.assertEqual(self.client.get("/health/").json()["status"], "ok")
