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

@register.filter(name='tax_plat')
def tax_plat(precio):

    precio_con_tax = ((precio * 10 ) / 100 )
    return precio_con_tax.quantize(Decimal('0.00'))


@register.filter(name='tax_trans')
def tax_trans(precio):
    precio_con_tax = (((precio * 3) / 100))
    return precio_con_tax.quantize(Decimal('0.00') + Decimal('0.50'))

@register.filter(name='tax_full')
def tax_full(precio):
    return precio.quantize(Decimal('0.00')) + tax_plat(precio) + tax_trans(precio)
