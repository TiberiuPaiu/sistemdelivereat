from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from myapp.models import Pedido, Cocina, Repartidor
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

class ListPedidosCocina(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = 'cocina'
    template_name = 'cocina/lista_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self):
        # Obtener el restaurante al que pertenece el usuario de cocina
        user_cocina = get_object_or_404(Cocina, user=self.request.user)

        # Filtrar los pedidos por restaurante y estados específicos

        pedidos = Pedido.objects.filter(
            restaurante=user_cocina.restaurante,
            estado__in=['preparacion', 'espera_preparacion']
        )

        query = self.request.GET.get('codigo_pedido')

        if query:
            pedidos = pedidos.filter(codigo_pedido__icontains=query)

        return pedidos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kanban'] = True

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
    pedido = get_object_or_404(Pedido,id=pedido_id)
    if pedido.estado == 'espera_preparacion':
        try:
            pedido.estado='preparacion'
            pedido.save()
            messages.success(request, "El pedido se paso se paso en estado de preparacion")
            return redirect("myapp:pedidos_actualizados")
        except Exception as e:
            messages.error(request, e)
            return redirect("myapp:pedidos_actualizados")
    messages.warning(request, "Se ha producido un error en el estado del pedido seleccionado.")
    return redirect("myapp:pedidos_actualizados")


def asignar_repartidor(request,pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if request.method == 'POST':
        try:
            repartidor = Repartidor.objects.get(id=request.POST['repartidor_id'])
            # Lógica para asignar el repartidor al pedido y cabiar estado
            pedido.repartidor = repartidor
            pedido.estado = 'espera_repartidor'
            pedido.save()
            messages.success(request, "El pedido se asignó correctamente.")
            return redirect("myapp:pedidos_actualizados")
        except Exception as e:
            messages.error(request, e)
            return redirect("myapp:pedidos_actualizados")



    ruta_pagina = [
        {
            'text': "Llistat de pedidos ",
            'link': "myapp:pedidos_actualizados",
        },

        {
            'text': "Asignar repartidor  ",
            'link': "",
        }
    ]

    title_pagina = [
        {
            'label_title': "VAsignar repartidor ",
            'title_card': "Asignar repartidor para la etrega de pedido "+pedido.codigo_pedido,
        }
    ]

    context = {
        'ruta_pagina': ruta_pagina,
        'title_pagina': title_pagina,
        'repardidores': Repartidor.objects.filter(restaurante=Cocina.objects.get(user=request.user).restaurante),

    }

    return render(request, 'cocina/asignar_repartidor.html', context)