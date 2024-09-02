import os

from behave import given, when, then
from django.urls import reverse
from django.test import Client
from myapp.models import User, Ubicacion, Restaurante, Partners, Negocio

from behave import given, when, then
from splinter.exceptions import ElementDoesNotExist
from django.urls import reverse



@given('estoy autenticado como partner con el nombre de usuario "{username}" y contraseña "{password}"')
def step_impl_authenticate(context, username, password):
    # Crear el usuario
    user = User.objects.create_user(username=username, password=password)
    user.user_type = 'partner'
    user.save()
    Partners.objects.create(user=user)

    # Iniciar sesión a través de la interfaz web
    context.browser.visit(context.get_url(''))
    form = context.browser.find_by_tag('form').first
    context.browser.fill('username', username)
    context.browser.fill('password', password)

    form.find_by_id('submit').first.click()

    assert context.browser.url.startswith(context.get_url('/lista/restaurantes/')), f"Se esperaba redirigir a la lista de restaurantes, pero se está en: {context.browser.url}"
    print("Contenido de la página después del inicio de sesión:", context.browser.html)
@when('añado un restaurante con los siguientes datos')
def step_impl_add_restaurant(context):
    # Navegar a la página de creación de restaurantes
    context.browser.visit(context.get_url('myapp:add_restaurante'))
    print("URL actual:", context.browser.url)

    for field in context.browser.find_by_tag('input'):
        print("Nombre del campo:", field['name'])

    # Extraer los datos del restaurante de la tabla
    data = context.table.rows[0]
    context.browser.fill('nombre_restaurante', data[0])
    context.browser.fill('descripcion', data[1])
    context.browser.fill('direcion', data[2])
    context.browser.fill('numero', data[3])
    context.browser.fill('codigo_postal', data[4])
    context.browser.fill('pais', data[5])
    context.browser.fill('ciudad', data[6])
    context.browser.fill('nombre_restaurante', data[0])
    # Subir la imagen (asegúrate de que la ruta sea correcta)
    archivos_path = os.path.join(os.path.dirname(__file__), 'test_files')
    context.browser.attach_file('imagenes', os.path.join(archivos_path, 'restaurante-4.jpg'))

    # Enviar el formulario
    context.browser.find_by_name('submit').click()


@then('debería ver el restaurante "{restaurant_name}" en la lista de mis restaurantes')
def step_impl_check_restaurant_in_list(context, restaurant_name):
    # Navegar a la lista de restaurantes
    context.browser.visit(context.get_url('myapp:list_restaurantes'))

    # Verificar que el restaurante aparezca en la página
    assert context.browser.is_text_present(
        restaurant_name), f"Se esperaba que el restaurante '{restaurant_name}' estuviera en la lista."