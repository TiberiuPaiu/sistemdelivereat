# crear_tipos_comida.py

from django.core.management.base import BaseCommand
from myapp.models import TipoComida

class Command(BaseCommand):
    help = 'Crea tipos de comida en la base de datos'

    def handle(self, *args, **kwargs):
        tipos_comida = [
            'Italiana',
            'Mexicana',
            'China',
            'Ensaladas',
            'Hamburguesas'
            # Agrega más tipos de comida según sea necesario
        ]

        for tipo in tipos_comida:
            TipoComida.objects.create(nombre=tipo)

        self.stdout.write(self.style.SUCCESS('Tipos de comida creados exitosamente'))