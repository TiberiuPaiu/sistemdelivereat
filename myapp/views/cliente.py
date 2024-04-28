from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Round, Cast
from myapp.models import Restaurante, Plato, Carrito, DetalleCarrito
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin


class RestauranteListClienteView( ListView):
    model = Restaurante
    #user_type_required = 'partners'
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


class PlatosListClienteView( ListView):
    model = Plato
    #user_type_required = 'partners'
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


def agregar_al_carrito(request, plato_id):
    plato = get_object_or_404(Plato, pk=plato_id)
    carrito_item, created = Carrito.objects.get_or_create(usuario=request.user, plato=plato)

    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        carrito_item.cantidad = cantidad
        carrito_item.save()
        return redirect('carrito_lista')

    context = {
        'plato': plato,
        'carrito_item': carrito_item,
    }

    return render(request, 'cliente/carito/agregar_al_carrito.html', context)


def carrito_lista(request):
    # Obtener todos los platos en el carrito del usuario actual
    platos_carrito = Carrito.objects.filter(usuario=request.user)

    context = {
        'platos_carrito': platos_carrito
    }

    return render(request, 'cliente/carito/carrito_lista.html', context)