import os

from behave import given, when, then
from django.contrib.auth.models import User
from myapp.models import User

from behave import given, when, then
from django.urls import reverse
from django.test import Client

@given(u'estoy en la página de registro de clientes')
def visit_registration_page(context):
    context.client = Client()
    context.response = context.client.get(reverse('myapp:hacer_registro_cliente'))
    assert context.response.status_code == 200

@when(u'lleno el formulario con los siguientes datos')
def fill_registration_form(context):
    for row in context.table:
        form = {
            'first_name': row['nombre'],
            'last_name': row['apellidos'],
            'email': row['email'],
            'telefono': row['telefono'],
            'prefix_tel': row['prefijo'],
            'username': row['username'],
            'password': row['password'],
            'pais': row['pais'],
            'ciudad': row['ciudad'],
            'codigo_postal': row['codigo_postal'],
            'direcion': row['direccion'],
            'numero': row['numero'],
        }
        context.data = form
        context.response = context.client.post(reverse('myapp:hacer_registro_cliente'), form,follow=True)
@when(u'envío el formulario')
def submit_registration_form(context):
    pass  # La acción de enviar el formulario ya se realiza en el paso 'when lleno el formulario...'

@then(u'debería ver la página de inicio de sesión')
def see_login_page(context):
    assert context.response.status_code == 200  # Debe ser 200 después de seguir la redirección
    assert 'Inicia sesión dentro del sistema de DeliveEreat' in context.response.content.decode('utf-8')
@then(u'debería ver la página de registro con el siguiente "{mesg_error}"')
def see_registration_page_with_errors(context,mesg_error):
    content = context.response.content.decode('utf-8')
    # Verificar si hay mensajes de error en el contenido
    assert mesg_error in content, "No se encontraron mensajes de error en el contenido de la respuesta."

@then(u'debería haber un username registrado con el username "{username}" con el siguiente rol "{rol}"')
def check_user_registered(context, username, rol):
    assert User.objects.filter(username=username).exists()
    user = User.objects.get(username=username)
    assert user.user_type == rol, f"El rol del usuario es {user.user_type}, pero se esperaba {rol}"



@then(u'debería de no existir el usuario con el username "{username}"')
def check_user_not_registered(context, username):
    assert not User.objects.filter(username=username).exists()



@given(u'estoy en la página de registro de partners')
def visit_registration_page(context):
    context.client = Client()
    context.response = context.client.get(reverse('myapp:hacer_registro'))
    assert context.response.status_code == 200


@then('debería ver la página de inicio de sesión de partners')
def see_login_page(context):
    assert context.response.status_code == 302


@when(u'lleno el formulario de partners con los siguientes datos')
def fill_registration_form(context):
    for row in context.table:
        form = {
            'username': row['username'],
            'email': row['email'],
            'password': row['password'],
            'prefix_tel': row['prefix_tel'],
            'telefono': row['telefono'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'nombre_negocio': row['nombre_negocio'],
        }

        archivos_path = os.path.join(os.path.dirname(__file__), 'test_files')
        archivos = [
            ('archivos', open(os.path.join(archivos_path, 'file1.pdf'), 'rb')),
            ('archivos', open(os.path.join(archivos_path, 'file2.pdf'), 'rb'))
        ]

        context.data = form
        context.response = context.client.post(reverse('myapp:hacer_registro_partner'), form, files=archivos)



