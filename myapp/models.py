
from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('partners', 'Partners'),
        ('repartidor', 'Repartidor'),
        ('cocina', 'Encargado de Cocina'),
        ('cliente', 'Cliente'),
        ('admin', 'Admistrador')
    ]
    user_type = models.CharField(
        max_length=255,
        choices=USER_TYPE_CHOICES,
        default='cliente',
    )
    prefix_tel = models.CharField(max_length=5)
    telefono = models.CharField(max_length=30)

class Negocio(models.Model):
    nombre = models.CharField(max_length=255)

class Partners(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='rolpartner')
    negocio = models.OneToOneField(Negocio, on_delete=models.CASCADE, null=True, related_name='negocio')


class Archivo(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='documentos_negocio/')