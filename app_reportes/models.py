from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    es_admin = models.BooleanField(default=False)
    area_responsable = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Reporte(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En curso', 'En curso'),
        ('Resuelto', 'Resuelto'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    def __str__(self):
        return f"Reporte de {self.usuario.user.username} - {self.estado}"


