from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, DeleteView
from rest_framework import viewsets

from myapp.models import Restaurante, Plato, ResenaRestaurante, ResenaPlato, Cliente, Pedido, Resena
from myapp.serializers import RestauranteSerializer
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from django.contrib import messages

from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required

class ResenasView( DetailView):
    template_name = 'admin/resenas.html'
    user_type_required = 'partners'

    def get_object(self):
        # Obtener el tipo de objeto y su ID desde la URL
        tipo_objeto = self.kwargs['tipo_objeto']
        id_objeto = self.kwargs['id_objeto']

        # Determinar qué modelo se está solicitando y obtener el objeto correspondiente
        if tipo_objeto == 'restaurante':
            return get_object_or_404(Restaurante, pk=id_objeto)
        elif tipo_objeto == 'plato':
            return get_object_or_404(Plato, pk=id_objeto)
        # Puedes agregar más tipos de objetos aquí según sea necesario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_objeto = self.kwargs['tipo_objeto']
        id_objeto = self.kwargs['id_objeto']
        context['objeto_id'] = id_objeto
        user_cliente = Cliente.objects.get(user=self.request.user)

        # Obtener todas las reseñas asociadas al restaurante o plato
        if tipo_objeto == 'restaurante':
            restaurante = context['object']
            context['resenas'] = restaurante.resenas.all()
            context['tipo'] ='restaurante'


            # Verificar si el usuario ha realizado un pedido en el restaurante y está finalizado
            user_has_ordered = Pedido.objects.filter(cliente=user_cliente, restaurante=restaurante).filter(estado='entregado').exists()
            context['user_has_reviewed'] = user_has_ordered

            context['title_pagina'] = {'label_title': "Reseñas para restaurante",
                                       'title_card': "Reseñas del restaurante " + restaurante.nombre,
                                       },

            context['ruta_pagina'] = [{
                    'text': "Lista de restaurantes",
                    'link': "myapp:restaurantes_list_cliente",
            },
                    {
                        'text': "Reseñas del restaurante " + restaurante.nombre,
                        'link': "",
                    }
            ]
        elif tipo_objeto == 'plato':
            plato = context['object']
            context['resenas'] = plato.resenas.all()
            context['tipo'] = 'plato'

            # Verificar si el usuario ha realizado un pedido del plato y está entregado
            user_has_ordered = Pedido.objects.filter(cliente=user_cliente, platos=plato).filter(estado='entregado').exists()
            context['user_has_reviewed'] = user_has_ordered

            context['title_pagina'] = {'label_title': "Reseñas para plato",
                                       'title_card': "Reseñas del plato " + plato.nombre,
                                       }


        context['tipo_objeto'] = tipo_objeto
        return context

    # views.py
@login_required
@web_access_type_required("cliente")
def crear_resena(request, tipo_objeto, id_objeto):
    if request.method == 'POST':

        if 'estrellas' not in request.POST or not request.POST['estrellas']:
            messages.error(request, 'Es obligatorio dejar una puntuacion.')
            return redirect('myapp:resena_generico', tipo_objeto=tipo_objeto, id_objeto=id_objeto)

        if tipo_objeto == 'restaurante':
            restaurante = get_object_or_404(Restaurante, id=id_objeto)

            if ResenaRestaurante.objects.filter(cliente=Cliente.objects.get(user=request.user), restaurante=restaurante).exists():
                messages.error(request, 'Ya has dejado una reseña para este restaurante.')
                return redirect('myapp:resena_generico',tipo_objeto='restaurante', id_objeto=id_objeto)

            resena = ResenaRestaurante(
                    cliente=Cliente.objects.get(user=request.user),
                    restaurante=restaurante,
                    comentario=request.POST['comentario'],
                    puntuacion=request.POST['estrellas']
            )
            resena.save()
            messages.success(request, 'Reseña guardada exitosamente.')
            return redirect('myapp:resena_generico',tipo_objeto='restaurante', id_objeto=id_objeto)

        elif tipo_objeto == 'plato':
            plato = get_object_or_404(Plato, id=id_objeto)

            if ResenaPlato.objects.filter(cliente=Cliente.objects.get(user=request.user), plato=plato).exists():
                messages.error(request, 'Ya has dejado una reseña para este plato.')
                return redirect('myapp:resena_generico', tipo_objeto='plato', id_objeto=id_objeto)

            resena = ResenaPlato(
                cliente=Cliente.objects.get(user=request.user),
                plato=plato,
                comentario=request.POST['comentario'],
                puntuacion=request.POST['estrellas']
            )
            resena.save()
            messages.success(request, 'Reseña guardada exitosamente.')
            return redirect('myapp:resena_generico', tipo_objeto='plato', id_objeto=id_objeto)

class BorrarResenaView(LoginRequiredMixin, RolRequiredMixin, DeleteView):
    user_type_required = 'cliente'

    def get_object(self, queryset=None):
        tipo_objeto = self.kwargs['tipo_objeto']

        if tipo_objeto == 'restaurante':
            self.model = ResenaRestaurante
        elif tipo_objeto == 'plato':
            self.model = ResenaPlato
        else:
            raise Http404('Página no encontrada')

        return super().get_object(queryset)

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'cliente'):
            return queryset.filter(cliente=Cliente.objects.get(user=self.request.user))
        else:
            return queryset.none()

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_objeto = self.kwargs['tipo_objeto']
        id_objeto = self.kwargs['id_objeto']

        if tipo_objeto == 'restaurante':
            messages.success(self.request, 'Reseña a sido elimnada.')
            return redirect('myapp:resena_generico', tipo_objeto='restaurante', id_objeto=id_objeto)

        elif tipo_objeto == 'plato':
            messages.success(self.request, 'Reseña a sido elimnada.')
            return redirect('myapp:resena_generico', tipo_objeto='plato', id_objeto=id_objeto)
        else:
            raise Http404('Página no encontrada')


