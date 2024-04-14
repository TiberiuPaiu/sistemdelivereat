from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from myapp.models import Restaurante, Plato


class ResenasView(DetailView):
    template_name = 'admin/resenas.html'

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

        # Obtener todas las reseñas asociadas al restaurante o plato
        if tipo_objeto == 'restaurante':
            restaurante = context['object']
            context['resenas'] = restaurante.resenas.all()

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
            context['title_pagina'] = {'label_title': "Reseñas para plato",
                                       'title_card': "Reseñas del plato " + plato.nombre,
                                       },
            context['ruta_pagina'] = [{
                'text': "Lista de restaurantes",
                'link': "myapp:list_restaurantes",
            },
                {
                    'text': "Listado platos del  " + plato.restaurante.nombre,
                    'link': "",
                },
                {
                    'text': "Reseñas del plato " + plato.nombre,
                    'link': "",
                }
            ]

        context['tipo_objeto'] = tipo_objeto
        return context