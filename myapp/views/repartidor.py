
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView ,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from myapp.models import Pedido, Cocina, Repartidor
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required

from django.contrib import messages

class ListPedidosRepartidor(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = 'repartidor'
    template_name = 'repartidor/lista_pedidos_recoger.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self):
        # Obtener el restaurante al que pertenece el usuario repartidor
        user_repartidor = Repartidor.objects.get(user=self.request.user)

        # Filtrar los pedidos por restaurante y estados específicos y para el repatidor corespondiente

        pedidos = Pedido.objects.filter(
                restaurante=user_repartidor.restaurante,
                estado__in=['espera_repartidor'],
                repartidor=user_repartidor
        )

        return pedidos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['title_pagina'] = {'label_title': "Llistat de pedidos para recoger ",
                                   'title_card': "Llistat de pedidos para recoger  "
                                   },

        return context

class ListPedidosRepartidor(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = 'repartidor'
    template_name = 'repartidor/lista_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self):
        # Obtener el restaurante al que pertenece el usuario repartidor
        user_repartidor = Repartidor.objects.get(user=self.request.user)

        # Filtrar los pedidos por restaurante y estados específicos y para el repatidor corespondiente

        pedidos = Pedido.objects.filter(
                restaurante=user_repartidor.restaurante,
                estado__in=['en_camino'],
                repartidor=user_repartidor
        )

        return pedidos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['title_pagina'] = {'label_title': "Llistat de pedidos para entregar ",
                                   'title_card': "Llistat de pedidos para entregar  "
                                   },

        return context

@login_required
@web_access_type_required("repartidor")
def recoger_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if pedido.estado == 'espera_repartidor':
        pedido.estado='en_camino'
        pedido.save()
        messages.success(request, "El pedido a sido recogido con exito")

    return redirect("myapp:pedidos_para_entregar")


@login_required
@web_access_type_required("repartidor")
def validar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
            # Procesar los datos del formulario si son válidos
        codigo_validacio = request.POST.get('codigo')

        if codigo_validacio == pedido.codigo_validacio:
            # Código de validación correcto, puedes marcar el pedido como validado
            try:
                pedido.estado = 'entregado'
                pedido.save()
                messages.success(request, "El pedido a sido entregado corectamente.")
                return redirect('myapp:pedidos_realizados')
            except Exception as e:
                messages.error(request,e)
                return redirect('myapp:validar_pedido', pedido_id=pedido_id)

        else:
            messages.error(request, "El codigo de validacio es incorrecto. Vuelva a intentarlo o si no ponte en contacto con el restaurante.")
            return redirect('myapp:validar_pedido', pedido_id=pedido_id)


    ruta_pagina = [
        {
            'text': "Lista de pedidos para entregar ",
            'link': "myapp:list_restaurantes",
        },

        {
            'text': "Validar Pedido  " + pedido.codigo_pedido,
            'link': "",
        }
    ]

    title_pagina = [
        {
            'label_title': "Validar Pedido ",
            'title_card': "Validar Pedido con el cliente "+pedido.cliente.user.get_full_name(),
        }
    ]

    context = {
        'ruta_pagina': ruta_pagina,
        'title_pagina': title_pagina

    }


    return render(request, 'repartidor/from_validacion_pedido.html', context)


class Map_Rpartidor(LoginRequiredMixin, RolRequiredMixin, DetailView):
    model = Pedido
    user_type_required = 'repartidor'
    template_name = 'repartidor/GPS.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['title_pagina'] = {'label_title': "Ubicación pedido ",
                                   'title_card': "Ubicación pedido"
                                   },

        return context
