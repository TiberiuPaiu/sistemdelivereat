from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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

    def full_telefono(self):
        return self.prefix_tel + " " + self.telefono


class Negocio(models.Model):
    nombre = models.CharField(max_length=255)

class Partners(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='partners_role')
    negocio = models.OneToOneField(Negocio, on_delete=models.CASCADE, null=True, related_name='partners')

    def __str__(self):
        return self.negocio.nombre



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


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='cliente_role')
    ubicacion = models.OneToOneField(Ubicacion, on_delete=models.CASCADE, null=True, related_name='cliente')

    def __str__(self):
        return self.ubicacion.ciudad
class Restaurante(models.Model):
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE, related_name='partner_restaurantes')
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


class TipoComida(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
class Plato(models.Model):
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='platos')
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    imagen = models.ImageField(upload_to='imagenes_plato/')
    tipo_comida = models.ForeignKey(TipoComida, on_delete=models.CASCADE, related_name='platos')

    def __str__(self):
        return self.nombre

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    plato =models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='ingredientes')

    def __str__(self):
        return self.nombre





class Resena(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    comentario = models.TextField()
    puntuacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class ResenaRestaurante(Resena):
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='resenas')

class ResenaPlato(Resena):
    plato = models.ForeignKey('Plato', on_delete=models.CASCADE, related_name='resenas')


class Pedido(models.Model):
    ESTADOS_TYPE = [
        ('espera_preparacion', 'En espera la preparación'),
        ('preparacion', 'En preparación'),
        ('espera_repartidor', 'Pendiente para su recogida por el repartidor'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
        ('pendiente_pago', 'Pendiente de pago'),

    ]

    estado = models.CharField(
        max_length=255,
        choices=ESTADOS_TYPE,
        default='espera_preparacion',
    )
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    platos = models.ManyToManyField(Plato)
    direccion_entrega = models.CharField(max_length=255)

    total = models.DecimalField(max_digits=10, decimal_places=2)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)



"""
class HorarioTrabajo(models.Model):
    DIA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    dia = models.CharField(max_length=20, choices=DIA_CHOICES)
    apertura = models.TimeField(null=True)
    cierre = models.TimeField(null=True)
    estado_local = models.CharField(max_length=20, choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado')],
                                    default='abierto')
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dia} - {self.apertura} a {self.cierre} ({self.estado_local})"


class DiaFestivo(models.Model):
    fecha = models.DateField()
    estado_local = models.CharField(max_length=20, choices=[('cerrado', 'Cerrado')],
                                    default='cerrado')
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
"""



