from django.http import HttpResponse
from django.shortcuts import render, redirect

from myapp.forms import RegistroFormulario
from myapp.models import User, Negocio, Partners, Archivo

def index(request):
    return render(request, 'hola.html')


def mi_pagina_registro(request):
    return render(request, 'registro.html')

def post_registro(request):
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


            return redirect('myapp:index')
    else:
        form = RegistroFormulario()

    return render(request, 'registro.html', {'form': form})