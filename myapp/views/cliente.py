from datetime import datetime
from decimal import Decimal

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Avg, Q, Subquery, OuterRef, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Round, Cast
from myapp.models import Restaurante, Plato, Cliente, Pedido, Ubicacion, TipoComida, PedidoPlato
from sistemdelivereat.utils.OpenStreetMap import Geocoder
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.carito_copras import CarritoDeCompras
from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required

from django.contrib import messages

stripe.api_key = 'sk_test_51PMYfiGF2SGr9v2Ept70FwVCMRnjM8pdznzqezNqqxb3nmOx2xKFV9tezdmUONwHliygMlXXIFejCtvSdaIs2Hmg00AbvQ91MU'


class RestauranteListClienteView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Restaurante
    user_type_required = ['cliente']
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
    user_type_required = ['cliente']
    template_name = 'cliente/lista_platos.html'
    context_object_name = 'platos'
    paginate_by = 10


    def get_queryset(self):
        restaurante_id = self.kwargs['restaurante_id']

        order_by = self.request.GET.get('order_by')
        order_direction = self.request.GET.get('order_direction')
        precio_min = self.request.GET.get('precio_min')
        precio_max = self.request.GET.get('precio_max')

        if precio_min and precio_max:
            try:
                precio_min = float(precio_min)
                precio_max = float(precio_max)
                if precio_min > precio_max:
                    messages.error(self.request, 'El precio mínimo no puede ser mayor que el precio máximo.')
                    return Plato.objects.none()
            except ValueError:
                messages.error(self.request, 'Los valores de precio deben ser números válidos.')
                return Plato.objects.none()

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

        if precio_min:
            platos = platos.filter(precio_final__gte=precio_min)
        if precio_max:
            platos = platos.filter(precio_final__lte=precio_max)

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
def tax(precio):
    precio_con_tax = precio + ((precio * 10 ) / 100 ) + ((precio * 3 ) / 100 )
    return precio_con_tax.quantize(Decimal('0.00') + Decimal('0.50') )
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
        total_general = sum(tax(restaurante['total']) for restaurante in totales_por_restaurante.values())
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





class Pedidos_realizadosView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = ['cliente']
    template_name = 'cliente/pedido/listado_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self):
        pedidos = Pedido.objects.filter(cliente=Cliente.objects.get(user = self.request.user )).order_by('-fecha_pedido')
        query = self.request.GET.get('query')
        estado_pedido = self.request.GET.get('estado')
        restaurante = self.request.GET.get('restaurante')
        data_inicio = self.request.GET.get('data_inicio')
        data_fin = self.request.GET.get('data_fin')

        if query:
            pedidos = pedidos.filter(
                Q(platos__nombre__icontains=query)
                # Q(codigo_pedido=query)
            )
        if estado_pedido:
            pedidos = pedidos.filter(
                Q(estado=estado_pedido)
            )
        if restaurante:
            pedidos = pedidos.filter(
                Q(restaurante_id=restaurante)
            )
        if data_inicio and data_fin:
            new_data_inicio = datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M')
            new_data_fin = datetime.strptime(data_fin, '%Y-%m-%dT%H:%M')
            pedidos = pedidos.filter(fecha_pedido__range=(new_data_inicio, new_data_fin))

            try:
                new_data_inicio = datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M')
                new_data_fin = datetime.strptime(data_fin, '%Y-%m-%dT%H:%M')
                if new_data_inicio > new_data_fin:
                    messages.error(self.request, 'La fecha inicial no puede ser posterior a la fecha final.')
                else:
                    pedidos = pedidos.filter(fecha_pedido__range=(new_data_inicio, new_data_fin))
            except ValueError:
                messages.error(self.request, 'El formato de la fecha no es correcto. Use el formato AAAA-MM-DDTHH:MM.')
                return redirect('myapp:pedidos_realizados', )

        return pedidos


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente_ciudad = get_object_or_404(Cliente, user=self.request.user).ubicacion.ciudad
        context['restaurantes'] = Restaurante.objects.filter(ubicacion__ciudad=cliente_ciudad)
        context['estados'] = [
            ('espera_preparacion', 'En espera la preparación'),
            ('preparacion', 'En preparación'),
            ('espera_repartidor', 'Pendiente para su recogida por el repartidor'),
            ('en_camino', 'En camino'),
            ('entregado', 'Entregado'),
            ('cancelado', 'Cancelado'),
        ]

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


@login_required
@web_access_type_required("cliente")
def procesar_pedido_from(request):

    cliente = Cliente.objects.get(user=request.user)

    title_pagina = [
        {'label_title': "Realizar el pedido",
         'title_card': "Realizar el pedido",}
    ]
    ruta_pagina = [
        {'text': "Lista de restaurantes", 'link': "myapp:restaurantes_list_cliente"},
        {'text': "Carrito de compras", 'link': "myapp:pagina_del_carrito"},
        {'text': "Realizar el pedido", 'link': ""},
    ]

    if request.method == 'POST':
            # Procesar los datos del formulario si son válidos

            geocoder = Geocoder()
            full_address = f"{request.POST.get('direcion')} {str(request.POST.get('numero'))}, {request.POST.get('ciudad')}, {request.POST.get('codigo_postal')}, {request.POST.get('pais')}"

            coordenadas = geocoder.obtener_coordenadas(full_address)

            if coordenadas:
                latitud, longitud = coordenadas
            else:
                messages.error(request, "No se encontró la dirección. Por favor ingrese la dirección.")
                return redirect('myapp:procesar_pedido_form')

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
                    platos_por_restaurante[restaurante_id]['total'] += descuento(plato) * carrito[str(plato.id)][
                        'cantidad']

                # Verificar si el token de Stripe está presente
                total_trasferencia=0
                restaurantes=""
                stripe_token = request.POST.get('stripeToken')
                if not stripe_token:
                    messages.error(request, "Error con el token de Stripe. Inténtalo de nuevo.")
                    return redirect('myapp:procesar_pedido_form')

                # Crear los pedidos dentro de una transacción
                with transaction.atomic():
                    for restaurante_id, data in platos_por_restaurante.items():
                        restaurante = Restaurante.objects.get(id=restaurante_id)
                        cliente = Cliente.objects.get(user=request.user)
                        platos_en_pedido = Plato.objects.filter(id__in=data['platos'])

                        total_pedido = data['total']
                        total_trasferencia += tax(total_pedido)
                        restaurantes=restaurantes+" "+ restaurante.nombre

                        # Crear una nueva ubicación para cada pedido
                        ubicacion_pedido = Ubicacion.objects.create(
                            direcion=request.POST.get('direcion'),
                            numero=request.POST.get('numero'),
                            codigo_postal=request.POST.get('codigo_postal'),
                            pais=request.POST.get('pais'),
                            ciudad=request.POST.get('ciudad'),
                            latitud=latitud,
                            longitud=longitud
                        )
                        # Crear el pedido con la ubicación única
                        pedido = Pedido.objects.create(
                            cliente=cliente,
                            ubicacion=ubicacion_pedido,
                            total=total_pedido,
                            restaurante=restaurante
                        )

                        for plato in platos_en_pedido:
                            cantidad = carrito[str(plato.id)]['cantidad']
                            subtotal = descuento(plato) * cantidad
                            PedidoPlato.objects.create(
                                pedido=pedido,
                                plato=plato,
                                cantidad=cantidad,
                                subtotal=subtotal
                            )

                # Crear una nueva carga de Stripe para cada restaurante
                try:
                    charge = stripe.Charge.create(
                                    amount=int(total_trasferencia * 100),  # Stripe maneja los montos en centavos
                                    currency='eur',
                                    description=f'Pago del pedido para los restaurantes: {restaurantes}',
                                    source=stripe_token
                    )
                except stripe.error.StripeError as e:
                    messages.error(request,
                                               f"Error en el procesamiento del pago para los restaurantes: {restaurantes}: {e.error.message}")
                    return redirect('myapp:procesar_pedido_form')

                # Limpiar el carrito de compras después de realizar los pedidos
                carrito.clear()
                # Actualizar la sesión con el carrito vacío
                request.session['carrito'] = {}
                request.session.modified = True

                messages.success(request, "El proceso de pedido se realizado exitosamente.")
                return redirect('myapp:pedidos_realizados')
            except Exception as e:
                # Manejo de excepciones
                messages.error(request, "Error al procesar el pedido:" + str(e))
                return redirect('myapp:pedidos_realizados')

    return render(request,'cliente/pedido/hacer_pedido.html',{
                       'cliente': cliente,
                       'title_pagina': title_pagina,
                       'ruta_pagina': ruta_pagina,
                   }
    )





