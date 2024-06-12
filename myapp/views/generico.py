from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.views.generic import DetailView


from myapp.models import Restaurante, User, Pedido
from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.To_PDF import render_to_pdf

from sistemdelivereat.utils.decorators import web_access_type_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



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








class Generar_pdf(LoginRequiredMixin, RolRequiredMixin, DetailView):
    user_type_required = ['partners', 'cliente']
    def get(self, request, *args, **kwargs):
        # Obtener el tipo de objeto y su ID desde la URL
        tipo_objeto = self.kwargs['tipo_objeto']
        id_objeto = self.kwargs['id_objeto']

        pedido = Pedido.objects.get(id=id_objeto)
        data = {
                'object':pedido,

        }

        pdf = render_to_pdf("pdf/template_pdf.html", data)#Funcion en otro archivo que renderiza
        return HttpResponse(pdf, content_type = "application/pdf")



