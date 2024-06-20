from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from myapp.models import ResenaRestaurante, ResenaPlato, Restaurante, Plato, User, Partners
from sistemdelivereat import settings


class Command(BaseCommand):
    help = 'Add cuenta banco a partners'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID del usuario al que se le añadirá la tarjeta')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        try:
            user = User.objects.get(pk=user_id)
            partners = Partners.objects.get(user=user)
            negocio = partners.negocio

            # Añadir los datos de la cuenta bancaria encriptados
            negocio.nombre="pepito"
            negocio.numero_de_enrutamiento = "110000000"
            negocio.numero_de_cuenta = "000123456789"
            negocio.save()  # Asegúrate de guardar los cambios
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

        self.stdout.write(self.style.SUCCESS('Usuario admin creadas exitosamente.'))