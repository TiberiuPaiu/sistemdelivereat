from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.views.generic import ListView

from myapp.models import Restaurante
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


