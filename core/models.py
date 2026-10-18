from django.db import models

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    asunto = models.CharField(max_length=200, blank=True, verbose_name="Asunto")
    mensaje = models.TextField(verbose_name="Mensaje")
    leido = models.BooleanField(default=False, verbose_name="¿Leído?")
    creado_el = models.DateTimeField(auto_now_add=True, verbose_name="Recibido el")

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ["-creado_el"]

    def __str__(self): return f"{self.nombre} - {self.asunto or 'Sin Asunto'}"
