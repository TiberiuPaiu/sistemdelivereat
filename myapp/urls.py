
from django.urls import path
from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView, logout_then_login ,LogoutView

app_name = "myapp"
urlpatterns = [

    path('', LoginView.as_view(), name='login'),
    path('registro/', post_registro, name='hacer_registro'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # DetalleGenerico
    path('detalle/<str:tipo_objeto>/<int:id_objeto>/', DetalleGenericoView.as_view(), name='detalle_generico'),

    #restaurante
    path('lista/restaurantes/', ArticleDetailView.as_view(), name='list_restaurantes'),
    path('anadir/restaurante/', post_add_restaurante, name='add_restaurante'),

    #user_repartidor_cocina
    path('anadir/trabajdor/repartidor/<int:restaurante_id>', add_user_reparidor, name='add_user_reparidor'  ),
    path('anadir/trabajdor/cocina/<int:restaurante_id>', add_user_cocina, name='add_user_cocina'  ),

    path('lista/trabajdores/<int:restaurante_id>', UsuariosRestauranteListView.as_view(), name='list_user_restaurant'),

    path('reset_password/<int:user_id>/<int:restaurante_id>/', reset_password, name='reset_password'),
    #platos
    path('restaurante/agregar_plato/<int:restaurante_id>/', agregar_plato, name='agregar_plato'),
    path('restaurante/listar_plato/<int:restaurante_id>/', PlatosRestauranteListView.as_view() , name='list_platos'),

    # resena
    path('resena/<str:tipo_objeto>/<int:id_objeto>/', ResenasView.as_view(), name='resena_generico'),

]

# Agregar la configuracion para servir archivos de medios
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# add Configuring static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
