from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Round, Cast
from myapp.models import Restaurante, Plato, Cliente, Pedido, Ubicacion
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.carito_copras import CarritoDeCompras
from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required


class RestauranteListClienteView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Restaurante
    user_type_required = 'cliente'
    template_name = 'cliente/lista_restaurantes.html'
    context_object_name = 'restaurantes'
    paginate_by = 10

    def get_queryset(self):
        restaurantes = Restaurante.objects.annotate(
            puntuacion_media=Avg('resenas__puntuacion')
        )
        return restaurantes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)



        context['title_pagina'] = {'label_title': "Llistado de restaurantes",
                                   'title_card': "Llistado de restaurantes " ,
                                   },



        return context


class PlatosListClienteView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Plato
    user_type_required = 'cliente'
    template_name = 'cliente/lista_platos.html'
    context_object_name = 'platos'
    paginate_by = 10


    def get_queryset(self):
        restaurante_id = self.kwargs['restaurante_id']

        platos = Plato.objects.filter(restaurante_id=restaurante_id).annotate(
            puntuacion_media=Avg('resenas__puntuacion')
        )

        for plato in platos:
            # Calcular el precio con descuento
            precio_con_descuento = plato.precio - (plato.precio * plato.descuento / 100)
            # Redondear el resultado a dos decimales
            precio_final = round(precio_con_descuento, 2)
            # Asignar el precio final al plato
            plato.precio_final = precio_final


        return platos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del restaurante de la URL
        restaurante_id = self.kwargs['restaurante_id']

        # Obtén el restaurante
        restaurante = Restaurante.objects.get(pk=restaurante_id)

        context['title_pagina'] = {'label_title': "Llistat de platos",
                                   'title_card': "Llistat de platos de " + restaurante.nombre,
                                   },
        context['ruta_pagina'] = [{
            'text': "Lista de restaurantes",
            'link': "myapp:restaurantes_list_cliente",
        },
            {
                'text': "Lista de los platos  de " + restaurante.nombre,
                'link': "",
            }
        ]
        context['restaurante_id'] = restaurante.id
        return context

def descuento(plato):
    return plato.precio * (1 - Decimal(str(plato.descuento)) / 100)

@login_required
@web_access_type_required("cliente")
def agregar_al_carrito(request, plato_id):
    carrito = CarritoDeCompras(request)
    carrito.agregar_plato(str(plato_id))
    return redirect('myapp:pagina_del_carrito')


@login_required
@web_access_type_required("cliente")
def carrito_lista(request):
    restaurante_actual_id=None
    carrito = CarritoDeCompras(request).obtener_carrito()
    platos_en_carrito = Plato.objects.filter(id__in=carrito.keys())

    # Calcular el total

    total = sum((carrito[str(plato.id)]['cantidad'] * descuento(plato)) for plato in
                platos_en_carrito)
    total_formateado = total.quantize(Decimal('0.01'))

    # Crear un diccionario para almacenar las cantidades de cada plato en el carrito
    cantidades_por_plato = {}
    for plato in platos_en_carrito:
        plato_id = str(plato.id)
        # Obtener la cantidad del plato en el carrito, si existe, de lo contrario establecer en 0
        cantidad = carrito.get(plato_id, {'cantidad': 0})['cantidad']
        cantidades_por_plato[plato_id] = cantidad

    title_pagina = {'label_title': "Carrito de compras",
                               'title_card': "Carrito de compras ",
                               },
    ruta_pagina = [{
        'text': "Lista de restaurantes",
        'link': "myapp:restaurantes_list_cliente",
    },
    {
            'text': "Carrito de compras",
            'link': "",
    }
    ]

    return render(request, 'cliente/carito/carrito_lista.html',
                  {'platos': platos_en_carrito, 'cantidades_por_plato': cantidades_por_plato,'total':total_formateado,"title_pagina":title_pagina,"ruta_pagina":ruta_pagina,"restaurante_actual_id":restaurante_actual_id})

@login_required
@web_access_type_required("cliente")
def eliminar_plato_carrito(request, plato_id):
    carrito = CarritoDeCompras(request)
    carrito.eliminar_plato(str(plato_id))
    return redirect('myapp:pagina_del_carrito')


@login_required
@web_access_type_required("cliente")
def quitar_plato_carrito(request, plato_id):
    carrito = CarritoDeCompras(request)
    carrito.quitar_plato(str(plato_id))
    return redirect('myapp:pagina_del_carrito')




@login_required
@web_access_type_required("cliente")
def procesar_pedido(request):
    try:
        # Procesar el carrito de compras y crear un nuevo pedido para cada restaurante
        carrito = CarritoDeCompras(request).obtener_carrito()
        platos_por_restaurante = {}  # Diccionario para agrupar los platos por restaurante

        # Agrupar los platos por restaurante
        plato_ids = carrito.keys()
        platos = Plato.objects.filter(id__in=plato_ids)
        for plato in platos:
            restaurante_id = plato.restaurante.id
            if restaurante_id not in platos_por_restaurante:
                platos_por_restaurante[restaurante_id] = {'platos': [], 'total': 0}
            platos_por_restaurante[restaurante_id]['platos'].append(plato.id)
            platos_por_restaurante[restaurante_id]['total'] += descuento(plato) * carrito[str(plato.id)]['cantidad']

        # Crear los pedidos dentro de una transacción
        with transaction.atomic():
            for restaurante_id, data in platos_por_restaurante.items():
                restaurante = Restaurante.objects.get(id=restaurante_id)
                cliente = Cliente.objects.get(user=request.user)
                platos_en_pedido = Plato.objects.filter(id__in=data['platos'])
                total_pedido = data['total']

                # Crear una nueva ubicación para cada pedido
                ubicacion_pedido = Ubicacion.objects.create(
                    direcion=cliente.ubicacion.direcion,
                    numero=cliente.ubicacion.numero,
                    codigo_postal=cliente.ubicacion.codigo_postal,
                    pais=cliente.ubicacion.pais,
                    ciudad=cliente.ubicacion.ciudad,
                    latitud=cliente.ubicacion.latitud,
                    longitud=cliente.ubicacion.longitud
                )

                # Crear el pedido con la ubicación única
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    ubicacion=ubicacion_pedido,
                    total=total_pedido,
                    restaurante=restaurante
                )
                pedido.platos.set(platos_en_pedido)

        # Limpiar el carrito de compras después de realizar los pedidos
        carrito.limpiar_carrito()

        return redirect('myapp:pedidos_realizados')
    except Exception as e:
        # Manejo de excepciones
        print(f"Error al procesar el pedido: {e}")
        return redirect('myapp:pedidos_realizados')



class Pedidos_realizadosView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = 'cliente'
    template_name = 'cliente/pedido/listado_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self):
        return Pedido.objects.filter(cliente=Cliente.objects.get(user = self.request.user ))



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title_pagina'] = {'label_title': "Llistat de pedidos realizados",
                                   'title_card': "Llistat de pedidos realizados "
                                   },
        context['ruta_pagina'] = [{
            'text': "Lista de restaurantes",
            'link': "myapp:restaurantes_list_cliente",
        },
            {
                'text': "Llistat de pedidos realizados ",
                'link': "",
            }
        ]

        return context
@login_required
@web_access_type_required("cliente")
def cancelar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if pedido.estado == 'espera_preparacion':
        pedido.estado='cancelado'
        pedido.save()
    return redirect("myapp:pedidos_realizados")