from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from myapp.models import ResenaRestaurante, ResenaPlato, Restaurante, Plato ,User
from sistemdelivereat import settings


class Command(BaseCommand):
    help = 'Crea automáticamente usuario admin'

    def handle(self, *args, **kwargs):

        username = "admin_sistem"
        email = "admin@localhost"
        password = settings.GLOBAL_PASSWORD
        user = User.objects.create_user(username=username, email=email, password=password)
        user.user_type="admin"
        user.save()




        self.stdout.write(self.style.SUCCESS('Usuario admin creadas exitosamente.'))