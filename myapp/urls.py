
from django.urls import path
from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static

app_name = "myapp"
urlpatterns = [

    path('', index, name='index'),
    path('registrar/usuario/', post_registro, name='hacer_registro'),
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




]

# Agregar la configuracion para servir archivos de medios
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# add Configuring static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
