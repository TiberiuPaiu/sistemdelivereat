# En el archivo crear_resenas.py

from django.core.management.base import BaseCommand

from django.utils import timezone
from faker import Faker
import random

from myapp.models import ResenaRestaurante, ResenaPlato, Restaurante, Plato ,User

class Command(BaseCommand):
    help = 'Crea automáticamente reseñas'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Crear usuarios clientes
        num_clientes = 3  # Puedes ajustar el número de usuarios que quieres crear
        for _ in range(num_clientes):
            username = fake.user_name()
            email = fake.email()
            password = fake.password(length=12)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

        # Obtener todos los restaurantes y platos
        restaurantes = Restaurante.objects.all()
        platos = Plato.objects.all()

        # Crear reseñas para cada restaurante
        for restaurante in restaurantes:
            # Seleccionar un usuario cliente aleatorio
            usuario = random.choice(User.objects.filter(is_staff=False))

            # Crear una reseña para el restaurante
            ResenaRestaurante.objects.create(
                usuario=usuario,
                restaurante=restaurante,
                comentario=f'Reseña aleatoria para {restaurante.nombre}',
                puntuacion=random.randint(1, 5),
                fecha_creacion=timezone.now()
            )

        # Crear reseñas para cada plato
        for plato in platos:
            # Seleccionar un usuario cliente aleatorio
            usuario = random.choice(User.objects.filter(is_staff=False))

            # Crear una reseña para el plato
            ResenaPlato.objects.create(
                usuario=usuario,
                plato=plato,
                comentario=f'Reseña aleatoria para {plato.nombre}',
                puntuacion=random.randint(1, 5),
                fecha_creacion=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Reseñas creadas exitosamente.'))