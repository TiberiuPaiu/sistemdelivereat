
from django.urls import path
from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static

app_name = "myapp"
urlpatterns = [

    path('', index, name='index'),
    path('registrar/usuario/', post_registro, name='hacer_registro'),


]

# Agregar la configuracion para servir archivos de medios
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# add Configuring static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
