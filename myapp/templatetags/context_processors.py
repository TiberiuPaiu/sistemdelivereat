from sistemdelivereat.utils.carito_copras import CarritoDeCompras


def carrito_context(request):
    carrito = CarritoDeCompras(request)
    carrito_items = carrito.carrito
    total_carrito = sum(item['cantidad'] for item in carrito_items.values())
    return {'total_carrito': total_carrito}