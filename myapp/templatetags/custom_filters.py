from django import template
from decimal import Decimal
register = template.Library()

@register.filter(name='custom_get')
def custom_get(dictionary, key):
    return dictionary.get(str(key))


@register.filter(name='descuento')
def descuento(plato):
    precio_con_descuento = plato.precio * (1 - Decimal(str(plato.descuento)) / 100)
    return precio_con_descuento.quantize(Decimal('0.00'))
