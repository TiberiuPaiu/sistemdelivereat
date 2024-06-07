from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from myapp.models import Restaurante, User, Pedido
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin




class DetalleGenericoView(LoginRequiredMixin, RolRequiredMixin, DetailView):
    template_name = 'admin/detalle_generico.html'
    user_type_required = ['partners', 'cliente']

    def get_object(self):
        # Obtener el tipo de objeto y su ID desde la URL
        tipo_objeto = self.kwargs['tipo_objeto']
        id_objeto = self.kwargs['id_objeto']

        # Determinar qué modelo se está solicitando y obtener el objeto correspondiente
        if tipo_objeto == 'restaurante':
            return Restaurante.objects.get(pk=id_objeto)
        elif tipo_objeto == 'usuario':
            return User.objects.get(pk=id_objeto)
        elif tipo_objeto == 'pedido':
            return Pedido.objects.get(id=id_objeto)
        # Puedes agregar más tipos de objetos aquí según sea necesario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_objeto'] = self.kwargs['tipo_objeto']
        return context

