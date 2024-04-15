from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from myapp.models import Partners, User


class PartnersListView( ListView):
    template_name = 'partners_list.html'
    model = Partners
    context_object_name = 'partners'
    paginate_by = 10

    def get_queryset(self):
        # Obtener solo los usuarios que sean del tipo 'partners'
        return Partners.objects.all()

def active_partners(request, id_user):
    user = User.objects.get(id=id_user)

    if user.is_active == 1:
        user.is_active = 0


    else:
        user.is_active = 1


    return redirect('myapp:list_partners')
