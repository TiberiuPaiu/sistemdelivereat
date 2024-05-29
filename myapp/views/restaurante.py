from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from rest_framework import generics

from myapp.forms import RestauranteForm, AddUserFormulario
from myapp.models import Restaurante, Ubicacion, Imagen, Negocio, User, Repartidor, Cocina, Plato, Ingrediente, \
    TipoComida, Partners, Pedido
from sistemdelivereat import settings
from sistemdelivereat.utils.OpenStreetMap import Geocoder

from django.views.generic.list import ListView

from sistemdelivereat.utils.RolRequiredMixin import RolRequiredMixin
from sistemdelivereat.utils.decorators import web_access_type_required



class ArticleDetailView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Restaurante
    user_type_required = 'partners'
    template_name = 'admin/list_restaurante.html'
    context_object_name = 'restaurantes'
    paginate_by = 3

    def get_queryset(self):
        # Obtener el restaurante al que pertenece el usuario de cocina
        user_partners = get_object_or_404(Partners, user=self.request.user)

        # Filtrar los pedidos por restaurante y estados específicos

        restarantes = Restaurante.objects.filter(
            partner=user_partners,
        )
        return restarantes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title_pagina'] = {'label_title': "Llistado de restaurantes",
                                   'title_card': "Llistado de restaurantes  " ,
                                   },
        context['ruta_pagina'] = [ {
            'button_text': "Crear restaurante",
            'link': "myapp:add_restaurante",
        }
        ]

        return context

@login_required
@web_access_type_required("partners")
def post_add_restaurante(request):
    if request.method == 'POST':
        form = RestauranteForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesa el formulario y crea un nuevo restaurante en la base de datos
            nombre_restaurante = form.cleaned_data['nombre_restaurante']
            pais = form.cleaned_data['pais']
            ciudad = form.cleaned_data['ciudad']
            codigo_postal = form.cleaned_data['codigo_postal']
            direcion = form.cleaned_data['direcion']
            numero = form.cleaned_data['numero']
            descripcion = form.cleaned_data['descripcion']
            imagenes = request.FILES.getlist('imagenes')


            geocoder = Geocoder()
            full_address = f"{direcion} {str(numero)}, {ciudad}, {codigo_postal}, {pais}"
            coordenadas = geocoder.obtener_coordenadas(full_address)
            if coordenadas:
                latitud, longitud = coordenadas

                ubicacion = Ubicacion.objects.create(
                    direcion=direcion,
                    numero=numero,
                    codigo_postal=codigo_postal,
                    pais=pais,
                    ciudad=ciudad,
                    latitud =latitud,
                    longitud =longitud,
                )
                restaurante = Restaurante.objects.create(
                    partner= Partners.objects.get(user=request.user),
                    nombre=nombre_restaurante,
                    descripcion=descripcion,
                    ubicacion = ubicacion,
                )
                for imagen in imagenes:
                    Imagen.objects.create(restaurante=restaurante, imagen=imagen)

                messages.success(request, 'El restaurante se creado exitosamente')
                return redirect('myapp:list_restaurantes')
            else:
                error = geocoder.error

    else:
        form = RestauranteForm()

    ruta_pagina = [
        {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },

        {
            'text': "Añadir restaurante",
            'link': "",
        }
    ]

    title_pagina = [
        {
        'label_title': "Añadir el restaurante",
        'title_card': "Añadir el restaurante",
         }
    ]
    ruta_pagina = [
        {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },

        {
            'text': "Añadir restaurante ",
            'link': "",
        }
    ]

    context = {
        'ruta_pagina': ruta_pagina,
        'title_pagina': title_pagina,
        'form': form
    }

    return render(request, 'admin/add_restaurante.html',  context)


@login_required
@web_access_type_required("partners")
def add_user_reparidor(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)
    if request.method == 'POST':
        form = AddUserFormulario(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario si son válidos
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = settings.GLOBAL_PASSWORD
            user_type = 'repartidor'
            prefix_tel = form.cleaned_data['prefix_tel']
            telefono = form.cleaned_data['telefono']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']


            # Crear el usuario
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            user.user_type = user_type
            user.prefix_tel = prefix_tel
            user.telefono = telefono
            user.save()
            Repartidor.objects.create(user=user, restaurante=restaurante )
            messages.success(request, 'El usuario con el rol de repartidor se creado exitosamente')

            return redirect('myapp:list_restaurantes')
    else:
        form = AddUserFormulario()

    ruta_pagina = [
        {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },

        {
            'text': "Añadir trabjador " + restaurante.nombre,
            'link': "",
        }
    ]

    title_pagina = [
        {
            'label_title': "Añadir un repartidor ",
            'title_card': "Añadir un repartidor " + restaurante.nombre,
        }
    ]
    context = {
        'ruta_pagina': ruta_pagina,
        'title_pagina': title_pagina,
        'form': "",
        'restaurante_id':restaurante.id,
    }

    return render(request, 'admin/user/add_user_repartidor.html', context)


@login_required
@web_access_type_required("partners")
def add_user_cocina(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)
    if request.method == 'POST':
        form = AddUserFormulario(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario si son válidos
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = settings.GLOBAL_PASSWORD
            user_type = 'cocina'
            prefix_tel = form.cleaned_data['prefix_tel']
            telefono = form.cleaned_data['telefono']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Crear el usuario
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            user.user_type = user_type
            user.prefix_tel = prefix_tel
            user.telefono = telefono
            user.save()
            Cocina.objects.create(user=user, restaurante=restaurante)
            messages.success(request, 'El usuario con el rol de resoposable cocina se creado exitosamente')
            return redirect('myapp:list_restaurantes')
    else:
        form = RestauranteForm()

    ruta_pagina = [
        {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },

        {
            'text': "Añadir trabjador "+restaurante.nombre,
            'link': "",
        }
    ]

    title_pagina = [
        {
            'label_title': "Añadir un resposable cocina ",
            'title_card': "Añadir un resposable cocina "+restaurante.nombre,
        }
    ]
    context = {
        'ruta_pagina': ruta_pagina,
        'title_pagina': title_pagina,
        'form': "",
        'restaurante_id':restaurante.id,
    }

    return render(request, 'admin/user/add_user_cocina.html', context)


class UsuariosRestauranteListView(LoginRequiredMixin, RolRequiredMixin,ListView):
    user_type_required = 'partners'
    template_name = 'admin/user/list_user.html'  # Nombre de tu plantilla
    context_object_name = 'usuarios'  # Nombre del objeto en el contexto
    paginate_by = 3


    def get_queryset(self):
        # Obtén el ID del restaurante de la URL
        restaurante_id = self.kwargs['restaurante_id']

        # Obtén el restaurante
        restaurante = Restaurante.objects.get(pk=restaurante_id)

        # Obtén los cocineros y repartidores del restaurante
        cocineros = Cocina.objects.filter(restaurante=restaurante)
        repartidores = Repartidor.objects.filter(restaurante=restaurante)



        # Luego, puedes obtener los usuarios asociados a los cocineros y repartidores
        usuarios_cocina = [cocinero.user for cocinero in cocineros]
        usuarios_repartidor = [repartidor.user for repartidor in repartidores]

        # Combina las listas de usuarios de cocineros y repartidores si es necesario
        usuarios_totales = usuarios_cocina + usuarios_repartidor

        return usuarios_totales

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del restaurante de la URL
        restaurante_id = self.kwargs['restaurante_id']

        # Obtén el restaurante
        restaurante = Restaurante.objects.get(pk=restaurante_id)


        context['title_pagina'] = {'label_title': "Llistat de trabajadores",
                                   'title_card': "Llistat de trabajadores de " + restaurante.nombre,
                                   },
        context['ruta_pagina'] = [ {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },
        {
            'text': "Lista de trabjadores de " + restaurante.nombre,
            'link': "",
        }
        ]
        context['restaurante_id'] = restaurante.id
        return context

@login_required
@web_access_type_required("partners")
def reset_password(request, user_id, restaurante_id):
    user = User.objects.get(id=user_id)


    # reset password
    user.set_password(settings.GLOBAL_PASSWORD)
    user.save()

    # Construir la URL de redirección


    url = reverse('myapp:list_user_restaurant', kwargs={'restaurante_id': restaurante_id})

    return redirect(url)


@login_required
@web_access_type_required("partners")
def agregar_plato(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)
    tipos_comida = TipoComida.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descuento = request.POST.get('descuento')
        ingredientes = request.POST.getlist('ingredientes')
        imagen = request.FILES.get('imagen')
        tipo_comida = TipoComida.objects.get(id=request.POST.get('tipo_comida'))

        print(ingredientes)

        # Guardar el plato
        plato = Plato.objects.create(nombre=nombre, precio=precio, descuento=descuento ,restaurante=restaurante , tipo_comida=tipo_comida, imagen =imagen)

        # Guardar los ingredientes
        for ingrediente in ingredientes:
            Ingrediente.objects.create(nombre=ingrediente, plato=plato)

        messages.success(request, 'Podiste añadir un nuevo plato exitosamente ')
        url = reverse('myapp:list_platos', kwargs={'restaurante_id': restaurante_id})
        return redirect(url)


    ruta_pagina = [
        {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },

        {
            'text': "Añadir plato en el  "+restaurante.nombre,
            'link': "",
        }
    ]

    title_pagina = [
        {
            'label_title': "Añadir un plato ",
            'title_card': "Añadir un plato para  "+restaurante.nombre,
        }
    ]
    context = {
        'ruta_pagina': ruta_pagina,
        'title_pagina': title_pagina,
        'form': "",
        'restaurante_id':restaurante.id,
        'tipos_comida':tipos_comida
    }

    return render(request, 'admin/platos/add_platos.html', context)


class PlatosRestauranteListView(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Plato
    user_type_required = 'partners'
    template_name = 'admin/platos/listado_platos.html'  # Reemplaza 'tu_template.html' por la ruta a tu template
    context_object_name = 'platos'
    paginate_by = 10

    def get_queryset(self):
        restaurante_id = self.kwargs['restaurante_id']
        return Plato.objects.filter(restaurante_id=restaurante_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del restaurante de la URL
        restaurante_id = self.kwargs['restaurante_id']

        # Obtén el restaurante
        restaurante = Restaurante.objects.get(pk=restaurante_id)


        context['title_pagina'] = {'label_title': "Llistat de platos",
                                   'title_card': "Llistat de platos de " + restaurante.nombre,
                                   },
        context['ruta_pagina'] = [ {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },
        {
            'text': "Lista de los platos  de " + restaurante.nombre,
            'link': "",
        }
        ]
        context['restaurante_id'] = restaurante.id
        return context


class DetalleGenericoView(LoginRequiredMixin, RolRequiredMixin, DetailView):
    template_name = 'admin/detalle_generico.html'
    user_type_required = 'partners'

    def get_object(self):
        # Obtener el tipo de objeto y su ID desde la URL
        tipo_objeto = self.kwargs['tipo_objeto']
        id_objeto = self.kwargs['id_objeto']

        # Determinar qué modelo se está solicitando y obtener el objeto correspondiente
        if tipo_objeto == 'restaurante':
            return Restaurante.objects.get(pk=id_objeto)
        elif tipo_objeto == 'usuario':
            return User.objects.get(pk=id_objeto)
        # Puedes agregar más tipos de objetos aquí según sea necesario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_objeto'] = self.kwargs['tipo_objeto']
        return context


@login_required
@web_access_type_required("partners")
def add_horarios(request, restaurante_id):
    restaurante = Restaurante.objects.get(id=restaurante_id)

    if request.method == 'POST':
        return redirect('myapp:list_restaurantes')

    ruta_pagina = [
            {
                'text': "Lista de restaurantes",
                'link': "myapp:list_restaurantes",
            },

            {
                'text': "Añadir un horario al restaurante  " + restaurante.nombre,
                'link': "",
            }
        ]

    title_pagina = [
            {
                'label_title': "Añadir un horario ",
                'title_card': "Añadir un horario al restaurante " + restaurante.nombre,
            }
        ]

    context = {
            'ruta_pagina': ruta_pagina,
            'title_pagina': title_pagina,
            'restaurante_id': restaurante.id
    }

    return render(request, 'admin/add_horario_restaurante.html', context)




class ListPedidosAdmin(LoginRequiredMixin, RolRequiredMixin, ListView):
    model = Pedido
    user_type_required = 'partners'
    template_name = 'admin/lista_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10


    def get_queryset(self, **kwargs):
        # Obtén el ID del restaurante de la URL
        restaurante_id = self.kwargs['restaurante_id']
        return Pedido.objects.filter(restaurante_id=restaurante_id).order_by('-fecha_pedido')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title_pagina'] = {'label_title': "Historial de pedidos",
                                   'title_card': "Historial de pedidos "
                                   },
        context['ruta_pagina'] = [{
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },
            {
                'text': "Historial de pedidos ",
                'link': "",
            }
        ]

        return context

