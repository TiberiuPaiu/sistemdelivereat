
from django.urls import path
from myapp.views import *

app_name = "myapp"
urlpatterns = [

    path('', index, name='index'),
    path('registrar/usuario/', post_registro, name='hacer_registro'),


]
