
from django.urls import path ,include
from rest_framework.routers import DefaultRouter

from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView, logout_then_login ,LogoutView



app_name = "myapp"
urlpatterns = [

    path('', LoginView.as_view(), name='login'),
    path('registro/', post_registro, name='hacer_registro'),
    path('cliente/registro/', post_registro_cliente, name='hacer_registro_cliente'),


    path('logout/', LogoutView.as_view(), name='logout'),

    # DetalleGenerico
    path('detalle/<str:tipo_objeto>/<int:id_objeto>/', login_required(DetalleGenericoView.as_view()), name='detalle_generico'),

    #restaurante
    path('lista/restaurantes/', login_required(ArticleDetailView.as_view()), name='list_restaurantes'),
    path('anadir/restaurante/', login_required(post_add_restaurante), name='add_restaurante'),

    #user_repartidor_cocina
    path('anadir/trabajdor/repartidor/<int:restaurante_id>', login_required(add_user_reparidor), name='add_user_reparidor'  ),
    path('anadir/trabajdor/cocina/<int:restaurante_id>', login_required(add_user_cocina), name='add_user_cocina'  ),

    path('lista/trabajdores/<int:restaurante_id>', login_required(UsuariosRestauranteListView.as_view()), name='list_user_restaurant'),

    path('reset_password/<int:user_id>/<int:restaurante_id>/', login_required(reset_password), name='reset_password'),
    #platos
    path('restaurante/agregar_plato/<int:restaurante_id>/', login_required(agregar_plato), name='agregar_plato'),
    path('restaurante/listar_plato/<int:restaurante_id>/', login_required(PlatosRestauranteListView.as_view()) , name='list_platos'),

    # resena
    path('resena/<str:tipo_objeto>/<int:id_objeto>/', ResenasView.as_view(), name='resena_generico'),

    #horarios res
    path('restaurante/add_horarios/<int:restaurante_id>/', login_required(add_horarios),name='add_horarios'),



    #admins
    path('lista/partners', PartnersListView.as_view(),  name='list_partners' ),
    path('acces/partners/<int:id_user>/', active_partners ,name='active_partners'),


    #cliente
    path('cliente/lista/restaurantes/', RestauranteListClienteView.as_view(), name='restaurantes_list_cliente'),
    path('cliente/lista/restaurante/<int:restaurante_id>/platos/', PlatosListClienteView.as_view(), name='platos_list_cliente'),

    #cliente-carito
    path('agregaralcarrito/<int:plato_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', carrito_lista, name='pagina_del_carrito'),

]

# Agregar la configuracion para servir archivos de medios
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# add Configuring static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
