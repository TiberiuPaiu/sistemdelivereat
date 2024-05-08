from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from myapp.models import Pedido, Cocina, Repartidor
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.decorators import web_access_type_required
from django.contrib.auth.decorators import login_required

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
        user_cocina = Cocina.objects.get(user=self.request.user)

        # Filtrar los pedidos por restaurante y estados específicos

        pedidos = Pedido.objects.filter(
            restaurante=user_cocina.restaurante,
            estado__in=['preparacion', 'espera_preparacion']
        )
        return pedidos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repartidores'] = Repartidor.objects.filter(
            restaurante=Cocina.objects.get(user=self.request.user).restaurante,
        )

        context['title_pagina'] = {'label_title': "Llistat de pedidos ",
                                   'title_card': "Llistat de pedidos  "
                                   },
        context['ruta_pagina'] = [{
            'text': "Llistat de pedidos",
            'link': "",
        }

        ]

        return context
    # conexiones SSE y envíe actualizaciones de los pedidos.
    """
    Para actualizar los pedidos de manera inmediata sin necesidad de recargar la página, se necesita utilizar tecnologías de comunicación en tiempo real, como el  Server-Sent Events (SSE). 
    Estas tecnologías permiten que el servidor envíe actualizaciones al cliente sin que este tenga que realizar una solicitud explícita.
    """


@login_required
@web_access_type_required("cocina")
def preparacion_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if pedido.estado == 'espera_preparacion':
        pedido.estado='preparacion'
        pedido.save()
    return redirect("myapp:lista_pedidos_cocina")


def asignar_repartidor(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        repartidor_id = request.POST.get('repartidor')

        try:
            pedido = Pedido.objects.get(id=pedido_id)
            repartidor = Repartidor.objects.get(id=repartidor_id)

            # Depuración: Imprimir los valores recibidos
            print(f"Pedido ID: {pedido_id}")
            print(f"Repartidor ID: {repartidor_id}")

            # Lógica para asignar el repartidor al pedido y cabiar estado
            pedido.repartidor = repartidor
            pedido.estado = 'espera_repartidor'
            pedido.save()

            return JsonResponse({'message': 'Repartidor asignado correctamente'})
        except Pedido.DoesNotExist:
            return JsonResponse({'error': 'Pedido no encontrado'}, status=404)
        except Repartidor.DoesNotExist:
            return JsonResponse({'error': 'Repartidor no encontrado'}, status=404)
        except Exception as e:
            # Depuración: Imprimir el error
            print(f"Error al asignar el repartidor: {str(e)}")
            return JsonResponse({'error': 'Error al asignar el repartidor'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)