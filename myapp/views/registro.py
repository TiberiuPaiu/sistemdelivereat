from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect


from myapp.forms import RegistroFormulario, RegistroClienteFormulario
from myapp.models import User, Negocio, Partners, Archivo, Ubicacion, Cliente


from sistemdelivereat.utils.OpenStreetMap import Geocoder

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

def mi_pagina_registro(request):
    return render(request, 'registration/registro.html')

def post_registro(request):

    titulo_pagina= "Pagina de registro"

    if request.method == 'POST':
        form = RegistroFormulario(request.POST, request.FILES)
        if form.is_valid():
            # Procesar los datos del formulario si son válidos
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = 'partners'
            prefix_tel = form.cleaned_data['prefix_tel']
            telefono = form.cleaned_data['telefono']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            nombre_negocio = form.cleaned_data['nombre_negocio']
            archivos = request.FILES.getlist('archivos')

            if archivos is not None:
                messages.error(request, "Es obligatorio añadir archivos de Licencias comerciales, permisos de salud y registros sanitarios")
                return redirect("myapp:hacer_registro")

            try:
                # Crear el usuario
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                                last_name=last_name)
                user.user_type = user_type
                user.prefix_tel = prefix_tel
                user.telefono = telefono
                user.save()

                # Crear un nuevo objeto Negocio con el nombre ingresado en el formulario
                negocio = Negocio.objects.create(nombre=nombre_negocio)

                # Asignar al usuario como Partners
                Partners.objects.create(user=user, negocio=negocio)

                # Manejar la carga de archivos

                for archivo in archivos:
                    Archivo.objects.create(negocio=negocio, archivo=archivo)

            except Exception as e:
                messages.error(request, e)
                return redirect("myapp:hacer_registro")

            return redirect('myapp:login')
        else:
            # Mostrar errores en el formulario
            for field in form:
                if field.errors:
                    for error in field.errors:
                        messages.error(request, error)

        return render(request, 'registration/registro.html', {'form': form, 'titulo_pagina': titulo_pagina})

    else:
        form = RegistroFormulario()

    return render(request, 'registration/registro.html', {'form': form, 'titulo_pagina': titulo_pagina})

def post_registro_cliente(request):
    titulo_pagina = "Pagina de registro para los Clientes"

    if request.method == 'POST':
        form = RegistroClienteFormulario(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario si son válidos
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = 'cliente'
            prefix_tel = form.cleaned_data['prefix_tel']
            telefono = form.cleaned_data['telefono']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            pais = form.cleaned_data['pais']
            ciudad = form.cleaned_data['ciudad']
            codigo_postal = form.cleaned_data['codigo_postal']
            direcion = form.cleaned_data['direcion']
            numero = form.cleaned_data['numero']

            # Crear el usuario
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
                    latitud=latitud,
                    longitud=longitud,
                )
                try:
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name,
                                                    last_name=last_name)
                    user.user_type = user_type
                    user.prefix_tel = prefix_tel
                    user.telefono = telefono
                    user.save()

                    Cliente.objects.create(user=user, ubicacion=ubicacion)

                except Exception as e:
                    messages.error(request, e)
                    return redirect("myapp:hacer_registro_cliente")

            else:
                messages.error(request, "No se encontró la dirección. Por favor ingrese la dirección.")
                return redirect('myapp:hacer_registro_cliente')

            return redirect('myapp:login')

        else:
            # Mostrar errores en el formulario
            for field in form:
                if field.errors:
                    for error in field.errors:
                        messages.error(request, error)
            return render(request, 'registration/registro_cliente.html', {'form': form, 'titulo_pagina': titulo_pagina})

    else:
        form = RegistroFormulario()

    return render(request, 'registration/registro_cliente.html', {'form': form, 'titulo_pagina': titulo_pagina})
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == 'cliente':
                return reverse_lazy('myapp:restaurantes_list_cliente')
            elif user.user_type == 'partners':
                return reverse_lazy('myapp:list_restaurantes')
            elif user.user_type == 'cocina':
                return reverse_lazy('myapp:pedidos_actualizados')
            elif user.user_type == 'repartidor':
                return reverse_lazy('myapp:pedidos_repartidor', kwargs={'tipo_objeto': 'recoger'} )

        return super().get_success_url()


