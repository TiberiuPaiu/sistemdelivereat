from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from rest_framework import viewsets

from myapp.models import Restaurante, Plato, ResenaRestaurante, ResenaPlato, Cliente
from myapp.serializers import RestauranteSerializer
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from django.contrib import messages

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

        # Obtener todas las reseñas asociadas al restaurante o plato
        if tipo_objeto == 'restaurante':
            restaurante = context['object']
            context['resenas'] = restaurante.resenas.all()
            context['tipo'] ='restaurante'
            context['user_has_reviewed'] = ResenaRestaurante.objects.filter(cliente = Cliente.objects.get(user=self.request.user),
                                                                 restaurante=restaurante).exists()

            context['title_pagina'] = {'label_title': "Reseñas para restaurante",
                                       'title_card': "Reseñas del restaurante " + restaurante.nombre,
                                       },

            context['ruta_pagina'] = [{
                    'text': "Lista de restaurantes",
                    'link': "myapp:list_restaurantes",
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

            context['user_has_reviewed'] = ResenaPlato.objects.filter(cliente = Cliente.objects.get(user=self.request.user), plato=plato).exists()

            context['title_pagina'] = {'label_title': "Reseñas para plato",
                                       'title_card': "Reseñas del plato " + plato.nombre,
                                       },
            context['ruta_pagina'] = [{
                'text': "Lista de restaurantes",
                'link': "myapp:list_restaurantes",
            },
                {
                    'text': "Lista de los platos  de " + plato.restaurante.nombre,
                    'parametro': "/restaurante/listar_plato/"+ str(plato.restaurante.id)+"/",
                },
                {
                    'text': "Reseñas del plato " + plato.nombre,
                    'link': "",
                }
            ]

        context['tipo_objeto'] = tipo_objeto
        return context

    # views.py

def crear_resena(request, tipo_objeto, id_objeto):
    if request.method == 'POST':
        if tipo_objeto == 'restaurante':
            restaurante = get_object_or_404(Restaurante, id=id_objeto)

            if ResenaRestaurante.objects.filter(cliente=Cliente.objects.get(user=request.user), restaurante=restaurante).exists():
                messages.error(request, 'Ya has dejado una reseña para este restaurante.')
                return redirect('myapp:resena_generico',tipo_objeto='restaurante', id_objeto=id_objeto)

            resena = ResenaRestaurante(
                    cliente=Cliente.objects.get(user=request.user),
                    restaurante=restaurante,
                    comentario=request.POST['comentario'],
                    puntuacion=request.POST['puntuacion']
            )
            resena.save()
            messages.success(request, 'Reseña guardada exitosamente.')
            return redirect('myapp:resena_generico',tipo_objeto='restaurante', id_objeto=id_objeto)

        elif tipo_objeto == 'plato':
            plato = get_object_or_404(Plato, id=id_objeto)

            if ResenaPlato.objects.filter(cliente=Cliente.objects.get(user=request.user), plato=plato).exists():
                messages.error(request, 'Ya has dejado una reseña para este restaurante.')
                return redirect('myapp:resena_generico', tipo_objeto='plato', id_objeto=id_objeto)

            resena = ResenaRestaurante(
                cliente=Cliente.objects.get(user=request.user),
                plato=plato,
                comentario=request.POST['comentario'],
                puntuacion=request.POST['puntuacion']
            )
            resena.save()
            messages.success(request, 'Reseña guardada exitosamente.')
            return redirect('myapp:resena_generico', tipo_objeto='plato', id_objeto=id_objeto)




