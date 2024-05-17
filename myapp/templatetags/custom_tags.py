from django import template

from myapp.models import Plato, Restaurante, Repartidor, Cocina, ResenaRestaurante, ResenaPlato
from sistemdelivereat.utils.carito_copras import CarritoDeCompras

register = template.Library()

@register.simple_tag
def platos_count_ddbb(restaurante_id):
    return Plato.objects.filter(restaurante_id=restaurante_id).count()

@register.simple_tag
def user_count_ddbb(restaurante_id):
     num_cocina = Cocina.objects.filter(restaurante_id=restaurante_id).count()
     num_repartidor = Repartidor.objects.filter(restaurante_id=restaurante_id).count()
     return num_cocina + num_repartidor


@register.simple_tag
def resena_count_ddbb(restaurante_id):
     return ResenaRestaurante.objects.filter(restaurante_id=restaurante_id).count()



@register.simple_tag
def resena_plato_count_ddbb(plato_id):
     return ResenaPlato.objects.filter(plato_id=plato_id).count()


