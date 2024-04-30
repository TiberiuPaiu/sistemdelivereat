from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Round, Cast
from myapp.models import Restaurante, Plato, Cliente
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

@login_required
@web_access_type_required("cliente")
def agregar_al_carrito(request, plato_id):
    carrito = CarritoDeCompras(request)
    carrito.agregar_plato(str(plato_id))
    return redirect('myapp:pagina_del_carrito')


@login_required
@web_access_type_required("cliente")
def carrito_lista(request):
    carrito = CarritoDeCompras(request).obtener_carrito()
    platos_en_carrito = Plato.objects.filter(id__in=carrito.keys())

    # Crear un diccionario para almacenar las cantidades de cada plato en el carrito
    cantidades_por_plato = {}
    for plato in platos_en_carrito:
        plato_id = str(plato.id)
        # Obtener la cantidad del plato en el carrito, si existe, de lo contrario establecer en 0
        cantidad = carrito.get(plato_id, {'cantidad': 0})['cantidad']
        cantidades_por_plato[plato_id] = cantidad

    return render(request, 'cliente/carito/carrito_lista.html',
                  {'platos': platos_en_carrito, 'cantidades_por_plato': cantidades_por_plato})

@login_required
@web_access_type_required("cliente")
def eliminar_plato_carrito(request, plato_id):
    carrito = CarritoDeCompras(request)
    carrito.eliminar_plato(plato_id)
    return redirect('myapp:pagina_del_carrito')



