import os


from myapp.models import User, Archivo, Partners, Negocio

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
        # Verificar inmediatamente después de enviar el formulario
        print("Datos del formulario enviados:", form)
        print("Código de estado de la respuesta:", context.response.status_code)
        print("Contenido de la respuesta:", context.response.content.decode('utf-8'))
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

@then(u'debería  existir solo "{namber_registred}" usuarios')
def check_namber_user_registered(context, namber_registred):
    assert int(namber_registred) == User.objects.all().count()

@given(u'estoy en la página de registro de partners')
def visit_registration_page(context):
    context.client = Client()
    context.response = context.client.get(reverse('myapp:hacer_registro'))
    assert context.response.status_code == 200

@when(u'lleno el formulario de partners con los siguientes datos')
def fill_registration_form(context):
    for row in context.table:
        archivos_path = os.path.join(os.path.dirname(__file__), 'test_files')
        archivos = [
            ('archivos', open(os.path.join(archivos_path, 'file1.pdf'), 'rb')),
            ('archivos', open(os.path.join(archivos_path, 'file2.pdf'), 'rb'))
        ]

        form = {
            'username': row['username'],
            'email': row['email'],
            'password': row['password'],
            'prefix_tel': row['prefix_tel'],
            'telefono': row['telefono'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'nombre_negocio': row['nombre_negocio'],
            'archivos': archivos,
        }

        context.data = form
        context.response = context.client.post(reverse('myapp:hacer_registro'), form, format='multipart', follow=True)
        #print("Datos del formulario enviados:", form)
        #print("Código de estado de la respuesta:", context.response.status_code)
        #print("Contenido de la respuesta:", context.response.content.decode('utf-8'))
@when(u'lleno el formulario de partners con los siguientes datos pero sin archivos')
def not_fill_registration_form(context):
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


        context.data = form
        context.response = context.client.post(reverse('myapp:hacer_registro'), form, files=None, follow=True)

@then('debería ver que los archivos fueron subidos correctamente para el usuario "{username}"')
def check_files_uploaded(context,username ):
    # Aquí verificas si los archivos están disponibles en tu aplicación
    try:
        user = User.objects.get(username=username)
        partner = Partners.objects.get(user=user)
        negocio = partner.negocio

        archivos_negocio = Archivo.objects.filter(negocio=negocio)
        assert archivos_negocio.exists(), f"No se encontraron archivos asociados al negocio de {partner}"

        # Verificar archivos específicos
        assert archivos_negocio.filter(archivo__icontains='file1.pdf').exists(), "No se encontró file1.pdf"
        assert archivos_negocio.filter(archivo__icontains='file2.pdf').exists(), "No se encontró file2.pdf"

    except User.DoesNotExist:
        raise AssertionError(f"El usuario con username '{username}' no existe en la base de datos")
    except Partners.DoesNotExist:
        raise AssertionError(f"No se encontró un partner asociado al usuario '{username}'")
    except Negocio.DoesNotExist:
        raise AssertionError(f"No se encontró un negocio asociado al partner de '{username}'")
    except Archivo.DoesNotExist:
        raise AssertionError(f"No se encontraron archivos asociados al negocio de {partner}")

@given(u'estoy en la página de inicio de sesión')
def visit_login_page(context):
    context.client = Client()
    context.response = context.client.get(reverse('myapp:login'))

@given(u'existen las sigentes cuentas registradas en el sistema')
def create_test_users(context):
    for row in context.table:
        user = User.objects.create_user(username=row['username'], password=row['password'])
        user.user_type = row['rol']
        user.save()
@when(u'ingreso mis credenciales')
def fill_login_form(context):
    for row in context.table:
        form = {
            'username': row['username'],
            'password': row['password'],
        }
        context.response = context.client.post(reverse('myapp:login'), form, follow=True)


@when(u'presiono el botón de iniciar sesión')
def press_login_button(context):
    pass  # Ya se realiza la acción de enviar el formulario en el paso anterior


@then(u'debería ser redirigido a la página corespodiente a mi rol')
def verify_redirection(context):

    assert context.client.session.get('_auth_user_id') is not None
    user = User.objects.get(id=context.client.session['_auth_user_id'])
    for row in context.table:
        if user.user_type == row['rol']:
            if row['rol'] == 'repartidor':
                expected_url = reverse('myapp:'+str(row['url']),   kwargs={'tipo_objeto': 'recoger'})
            else:
                expected_url = reverse('myapp:'+str(row['url']))
            print(f"Expected URL: {expected_url}")
            print(f"Redirect chain: {context.response.redirect_chain}")
            assert expected_url in context.response.redirect_chain[-1][0]