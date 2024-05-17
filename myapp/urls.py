
from django.urls import path ,include
from rest_framework.routers import DefaultRouter

from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView, logout_then_login ,LogoutView



app_name = "myapp"
urlpatterns = [

    path('', CustomLoginView.as_view(), name='login'),
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
    path('resena/<str:tipo_objeto>/<int:id_objeto>/',  login_required(ResenasView.as_view()), name='resena_generico'),
    path('resena/crear/<str:tipo_objeto>/<int:id_objeto>/', login_required(crear_resena), name='crear_una_resena'),

    path('resena/<str:tipo_objeto>/<int:id_objeto>/admin/',  login_required(ResenasAdminView.as_view()), name='resena_generico_admin'),

    path('resenas/<str:tipo_objeto>/<int:id_objeto>/borrar/<int:pk>/', login_required(BorrarResenaView.as_view()), name='borrar_resena'),

    #horarios res
    path('restaurante/add_horarios/<int:restaurante_id>/', login_required(add_horarios), name='add_horarios'),



    #admins
    path('lista/partners', PartnersListView.as_view(),  name='list_partners' ),
    path('acces/partners/<int:id_user>/', active_partners,name='active_partners'),


    #cliente
    path('cliente/lista/restaurantes/', login_required(RestauranteListClienteView.as_view()), name='restaurantes_list_cliente'),
    path('cliente/lista/restaurante/<int:restaurante_id>/platos/', login_required(PlatosListClienteView.as_view()), name='platos_list_cliente'),

    #cliente-carito
    path('agregaralcarrito/<int:plato_id>/', login_required(agregar_al_carrito), name='agregar_carrito'),
    path('carrito/',  login_required(carrito_lista), name='pagina_del_carrito'),
    path('quitar_plato_carrito/<int:plato_id>/', login_required(quitar_plato_carrito),
         name='quitar_plato_carrito'),

    path('eliminar/plato/carrito/<int:plato_id>/',  login_required(eliminar_plato_carrito), name='eliminar_plato_carrito'),
    path('carrito/borrar/', login_required(borrar_carrito), name='borrar_carrito'),

    #pedidos
    path('procesar_pedido/',  login_required(procesar_pedido), name='procesar_pedido'),
    path('pedidos_realizados/', login_required(Pedidos_realizadosView.as_view()) , name='pedidos_realizados'),
    path('pedido/<int:pedido_id>/cancelar/', login_required(cancelar_pedido), name='cancelar_pedido'),



    #cocina
    path('pedidos_actualizados/', login_required(ListPedidosCocina.as_view()), name='pedidos_actualizados'),
    path('pedido/<int:pedido_id>/preparacion/', login_required(preparacion_pedido), name='preparacion_pedido'),
    path('asignar_repartidor/<int:pedido_id>', asignar_repartidor, name='asignar_repartidor'),

    #repartidor
    path('pedidos/para/<str:tipo_objeto>/', login_required(ListPedidosRepartidor.as_view()), name='pedidos_repartidor'),
    #path('pedidos/para/entregar/', login_required(ListPedidosRepartidor.as_view()), name='pedidos_para_entregar'),
    #path('pedidos/entregados/', login_required(ListPedidosParaRecoger.as_view()), name='pedidos_para_recoger'),
    path('pedidos/<int:pedido_id>/recoger_pedido/', login_required(recoger_pedido), name='recoger_pedido'),
    path('pedido/<int:pk>/map', login_required(Map_Rpartidor.as_view()), name='map_rpartidor'),
    path('pedidos/<int:pedido_id>/validar_pedido/', login_required(validar_pedido), name='validar_pedido'),




]

# Agregar la configuracion para servir archivos de medios
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# add Configuring static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
