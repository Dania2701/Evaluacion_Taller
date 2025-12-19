from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    es_admin = models.BooleanField(default=False)
    area_responsable = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Reporte(models.Model):

    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En curso'),
        ('resuelto', 'Resuelto'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reportes'
    )

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()

    latitud = models.DecimalField(
        max_digits=10,
        decimal_places=6
    )
    longitud = models.DecimalField(
        max_digits=10,
        decimal_places=6
    )

    referencia = models.CharField(
        max_length=255,
        blank=True
    )

    foto = models.ImageField(
        upload_to='fotos_reportes/',
        blank=True,
        null=True
    )

    fecha_reporte = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_CHOICES,
        default='pendiente'
    )

    def __str__(self):
        return f"{self.titulo} - {self.get_estado_display()}"