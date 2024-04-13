from django.core.validators import MinValueValidator, MaxValueValidator
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

class Ubicacion(models.Model):
    direcion = models.CharField(max_length=255)
    numero = models.IntegerField()
    codigo_postal = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    latitud = models.CharField(max_length=255)
    longitud = models.CharField(max_length=255)

    def full_address(self):
       full_address = f"{self.direcion} {self.numero}, {self.codigo_postal}, {self.ciudad}, {self.pais}"
       return full_address



class Restaurante(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='restaurantes')
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    ubicacion = models.OneToOneField(Ubicacion, on_delete=models.CASCADE, null=True, related_name='ubicaciones')


    def __str__(self):
        return self.ubicacion



class Imagen(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='imagens')
    imagen = models.ImageField(upload_to='imagenes_restaurante/')


class Repartidor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='repartidor_user')
    restaurante = models.OneToOneField(Restaurante, on_delete=models.CASCADE, null=True, related_name='repartidor_restaurante')


class Cocina(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='cocina_user')
    restaurante = models.OneToOneField(Restaurante, on_delete=models.CASCADE, null=True, related_name='cocina_restaurante')


class Plato(models.Model):
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='platos')
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    plato =models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='ingredientes')




