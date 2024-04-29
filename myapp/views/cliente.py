from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Round, Cast
from myapp.models import Restaurante, Plato, Carrito, DetalleCarrito, Cliente
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
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

def agregar_al_carrito(request, plato_id):

    plato = get_object_or_404(Plato, pk=plato_id)
    if request.method == 'POST':

        cantidad = int(request.POST.get('cantidad', 1))  # Obtener la cantidad del formulario

        # Verificar si el usuario tiene un carrito existente
        carrito, creado = Carrito.objects.get_or_create(cliente=Cliente.objects.get(user =request.user))

        # Verificar si el plato ya está en el carrito del usuario
        detalle_carrito, creado = DetalleCarrito.objects.get_or_create(carrito=carrito, plato=plato)

        if not creado:
            # El plato ya está en el carrito, actualizar la cantidad
            detalle_carrito.cantidad += cantidad
            detalle_carrito.save()
        else:
            # El plato no está en el carrito, crear un nuevo detalle de carrito
            DetalleCarrito.objects.create(carrito=carrito, plato=plato, cantidad=cantidad)

        return redirect('myapp:pagina_del_carrito')


    return render(request, 'cliente/carito/agregar_al_carrito.html' ,)

@login_required
@web_access_type_required("cliente")
def carrito_lista(request):
    # Obtener todos los platos en el carrito del usuario actual
    carrito = Carrito.objects.filter(cliente=Cliente.objects.get(user =request.user))

    context = {
        'platos_carrito': carrito
    }

    return render(request, 'cliente/carito/carrito_lista.html', context)

@login_required
@web_access_type_required("cliente")
def restablecer_carrito(request):
    # Obtener el carrito del usuario actual
    carrito = Carrito.objects.filter(cliente=Cliente.objects.get(user =request.user)).first()
    if carrito:
        # Eliminar todos los detalles del carrito asociados a ese usuario
        carrito.detalles.all().delete()
        return redirect('myapp:pagina_del_carrito')
    else:
        return redirect('myapp:pagina_del_carrito')
