from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from myapp.models import Pedido, Cocina
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required

class ListPedidosCocina(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = 'cocina'
    template_name = 'cocina/lista_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self):
        # Obtener el restaurante al que pertenece el usuario de cocina
        user_cocina = Cocina.objects.get(user=self.request.user)

        # Filtrar los pedidos por restaurante y estados específicos

        pedidos = Pedido.objects.filter(
            restaurante=user_cocina.restaurante,
            estado__in=['preparacion', 'espera_preparacion']
        )
        return pedidos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title_pagina'] = {'label_title': "Llistat de pedidos ",
                                   'title_card': "Llistat de pedidos  "
                                   },
        context['ruta_pagina'] = [{
            'text': "Llistat de pedidos",
            'link': "",
        }

        ]

        return context

@login_required
@web_access_type_required("cocina")
def preparacion_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if pedido.estado == 'espera_preparacion':
        pedido.estado='preparacion'
        pedido.save()
    return redirect("myapp:lista_pedidos_cocina")
    
