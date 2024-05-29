from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Avg, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Round, Cast
from myapp.models import Restaurante, Plato, Cliente, Pedido, Ubicacion, TipoComida
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.carito_copras import CarritoDeCompras
from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required

from django.contrib import messages

class RestauranteListClienteView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Restaurante
    user_type_required = 'cliente'
    template_name = 'cliente/lista_restaurantes.html'
    context_object_name = 'restaurantes'
    paginate_by = 10

    def get_queryset(self):
        cliente_ciudad=get_object_or_404(Cliente, user=self.request.user).ubicacion.ciudad
        restaurantes = Restaurante.objects.filter(ubicacion__ciudad=cliente_ciudad).annotate(
            puntuacion_media=Avg('resenas__puntuacion')
        ).order_by('-puntuacion_media')

        query = self.request.GET.get('query')

        if query:
            restaurantes = restaurantes.filter(
                Q(nombre=query) |
                Q(ubicacion__direcion__icontains=query)

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

        order_by = self.request.GET.get('order_by')
        order_direction = self.request.GET.get('order_direction')

        platos = Plato.objects.filter(restaurante_id=restaurante_id).annotate(
            puntuacion_media=Avg('resenas__puntuacion'),
            precio_final=(F('precio') - (F('precio') * F('descuento') / 100))
        )

        if order_by == "precio":
            if order_direction == "asc":
                platos = platos.order_by('precio_final')
            elif order_direction == "desc":
                platos = platos.order_by('-precio_final')
        else:
            platos = platos.order_by('-puntuacion_media')

        query = self.request.GET.get('query')
        tipo_comida = self.request.GET.get('tipo_comida')
        if query:
            platos = platos.filter(
                Q(nombre__icontains=query)

            )
        if tipo_comida:
            platos = platos.filter(
                Q(tipo_comida__nombre=tipo_comida)

            )
        return platos


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del restaurante de la URL
        restaurante_id = self.kwargs['restaurante_id']

        context['tipos_comida'] = TipoComida.objects.filter(platos_tipo_comida__in=self.get_queryset()).distinct()

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
    precio_con_descuento = plato.precio * (1 - Decimal(str(plato.descuento)) / 100)
    return precio_con_descuento.quantize(Decimal('0.00'))

@login_required
@web_access_type_required("cliente")
def agregar_al_carrito(request, plato_id):
    carrito = CarritoDeCompras(request)
    carrito.agregar_plato(str(plato_id))
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@web_access_type_required("cliente")
def carrito_lista(request):
    carrito = CarritoDeCompras(request).obtener_carrito()
    platos_en_carrito = Plato.objects.filter(id__in=carrito.keys())


    # Verificar si el carrito está vacío
    if not platos_en_carrito:
        total_formateado = Decimal('0.00')
        totales_por_restaurante = {}
    else:
        # Calcular el total por restaurante
        totales_por_restaurante = {}
        for plato in platos_en_carrito:
            restaurante_id = plato.restaurante.id
            plato_id = str(plato.id)
            cantidad = carrito.get(plato_id, {'cantidad': 0})['cantidad']
            precio_final = descuento(plato)

            if restaurante_id not in totales_por_restaurante:
                totales_por_restaurante[restaurante_id] = {
                    'nombre': plato.restaurante.nombre,
                    'total': 0
                }

            totales_por_restaurante[restaurante_id]['total'] += cantidad * precio_final

        # Calcular el total general
        total_general = sum(restaurante['total'] for restaurante in totales_por_restaurante.values())
        total_formateado = Decimal(str(total_general)).quantize(Decimal('0.01'))

    # Crear un diccionario para almacenar las cantidades de cada plato en el carrito
    cantidades_por_plato = {}
    for plato in platos_en_carrito:
        plato_id = str(plato.id)
        cantidad = carrito.get(plato_id, {'cantidad': 0})['cantidad']
        cantidades_por_plato[plato_id] = cantidad


    title_pagina = [
        {'label_title': "Carrito de compras",
         'title_card': "Carrito de compras "}
    ]
    ruta_pagina = [
        {'text': "Lista de restaurantes", 'link': "myapp:restaurantes_list_cliente"},
        {'text': "Carrito de compras", 'link': ""}
    ]

    return render(request, 'cliente/carito/carrito_lista.html', {
        'platos': platos_en_carrito,
        'cantidades_por_plato': cantidades_por_plato,
        'total': total_formateado,
        'totales_por_restaurante': totales_por_restaurante,
        'title_pagina': title_pagina,
        'ruta_pagina': ruta_pagina,
    })
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
def borrar_carrito(request):
    carrito = CarritoDeCompras(request)
    carrito.borrar_carrito()
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
        carrito.clear()
        # Actualizar la sesión con el carrito vacío
        request.session['carrito'] = {}
        request.session.modified = True

        messages.success(request, "Se ha realizado la comada.")
        return redirect('myapp:pedidos_realizados')
    except Exception as e:
        # Manejo de excepciones
        messages.error(request, "Error al procesar el pedido:"+str(e))
        return redirect('myapp:pedidos_realizados')



class Pedidos_realizadosView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = 'cliente'
    template_name = 'cliente/pedido/listado_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self):
        return Pedido.objects.filter(cliente=Cliente.objects.get(user = self.request.user )).order_by('-fecha_pedido')



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
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado == 'espera_preparacion':
        try:
            pedido.estado = 'cancelado'
            pedido.save()
            messages.success(request, "El pedido se a cancelado exitosamente.")
            return redirect("myapp:pedidos_realizados")
        except Exception as e:
            messages.error(request, e)
            return redirect("myapp:pedidos_realizados")
    messages.warning(request, "Se ha producido un error en el momento de cancelar el pedido.")
    return redirect("myapp:pedidos_realizados")


