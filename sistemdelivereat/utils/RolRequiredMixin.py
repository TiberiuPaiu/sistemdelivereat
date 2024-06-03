from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

class RolRequiredMixin(AccessMixin):
    """
    Requiere que el usuario esté autenticado y tenga al menos uno de los roles especificados para acceder a la vista.
    Si el usuario no está autenticado o no tiene al menos uno de los roles especificados, se redirige a la página de inicio de sesión.
    """
    user_type_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.check_user_roles(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def check_user_roles(self, user):
        return user.user_type in self.user_type_required

    def handle_no_permission(self):
        return redirect('myapp:login')

