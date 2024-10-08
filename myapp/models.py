from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

from sistemdelivereat.settings import MEDIA_URL, STATIC_URL, ENCRYPTION_KEY
from cryptography.fernet import Fernet
from django.utils.functional import cached_property

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
    path_profile_photo = models.FileField(upload_to='profile_photo', null=True, blank=True)

    def full_telefono(self):
        return self.prefix_tel + " " + self.telefono

    def get_img(self):
        if self.path_profile_photo == None or self.path_profile_photo =="":
            return MEDIA_URL + "/img/user-150x150.png"
        else:
            return MEDIA_URL + "/profile_photo/" + str(self.path_profile_photo)


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
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True, related_name='repartidores')


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
    tipo_comida = models.ForeignKey(TipoComida, on_delete=models.CASCADE, related_name='platos_tipo_comida')

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
        ('espera_preparacion', 'En espera de la preparación'),
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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    platos = models.ManyToManyField(Plato, through='PedidoPlato')
    ubicacion = models.OneToOneField(Ubicacion, on_delete=models.CASCADE, null=True, related_name='pedido_ubicacion')

    total = models.DecimalField(max_digits=10, decimal_places=2)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    repartidor = models.ForeignKey(Repartidor, on_delete=models.CASCADE, null=True,  related_name='repartidor_asignado')
    # Otros campos relevantes del modelo
    codigo_pedido = models.CharField(max_length=50, unique=True)
    codigo_validacio = models.CharField(max_length=50, unique=True, null=True)


    def save(self, *args, **kwargs):
        if not self.codigo_pedido:
            # Generar un código único para el pedido de 12 caracteres
            unique_id_pedido = uuid.uuid4().hex[:12]
            unique_id_validacio = uuid.uuid4().hex[:12]
            self.codigo_pedido = unique_id_pedido
            self.codigo_validacio = unique_id_validacio
        super(Pedido, self).save(*args, **kwargs)

class PedidoPlato(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)




