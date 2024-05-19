from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Decorador para restringir el acceso a vistas solo a usuarios con el tipo 'cliente', 'repartidor' , 'partners' , etc.


def web_access_type_required(user_type):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_type == user_type:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('myapp:login')
        return wrapper
    return decorator

