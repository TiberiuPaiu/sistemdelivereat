from django import forms
from django.core.exceptions import ValidationError

from myapp.models import User, Restaurante, Ubicacion


class RegistroFormulario(forms.Form):
    nombre_negocio =forms.CharField(max_length=50, required=True,
                               error_messages={'required': 'El nombre del negocio de usuario es obligatorio'})
    username = forms.CharField(max_length=50, required=True,
                               error_messages={'required': 'El nombre de usuario es obligatorio'})
    email = forms.EmailField(label='Correo electrónico', required=True,
                             error_messages={'required': 'El correo electrónico es obligatorio'})
    password = forms.CharField(widget=forms.PasswordInput, max_length=128, min_length=8, required=True,
                               error_messages={'required': 'La contraseña es obligatoria',
                                               'max_length': 'El campo nombre no puede ser tan largo.',
                                               'min_length': 'La contraseña tiene que contener 8 caracteres'})
    prefix_tel = forms.CharField(max_length=3, required=True,
                                 error_messages={'required': 'Seleccione un prefijo'})
    telefono = forms.CharField(max_length=10, required=True,
                               error_messages={'required': 'El teléfono es obligatorio'})
    first_name = forms.CharField(max_length=50, required=True,
                                 error_messages={'required': 'El nombre es obligatorio'})
    last_name = forms.CharField(max_length=50, required=True,
                                error_messages={'required': 'El apellido es obligatorio'})
    archivos=forms.ClearableFileInput(attrs={"allow_multiple_selected": True})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': "El nombre de usuario ya existe"})






class AddUserFormulario(forms.Form):
    username = forms.CharField(max_length=50, required=True,
                               error_messages={'required': 'El nombre de usuario es obligatorio'})
    email = forms.EmailField(label='Correo electrónico', required=True,
                             error_messages={'required': 'El correo electrónico es obligatorio'})
    password = forms.CharField(widget=forms.PasswordInput, max_length=128, min_length=8, required=True,
                               error_messages={'required': 'La contraseña es obligatoria',
                                               'max_length': 'El campo nombre no puede ser tan largo.',
                                               'min_length': 'La contraseña tiene que contener 8 caracteres'})
    prefix_tel = forms.CharField(max_length=3, required=True,
                                 error_messages={'required': 'Seleccione un prefijo'})
    telefono = forms.CharField(max_length=10, required=True,
                               error_messages={'required': 'El teléfono es obligatorio'})
    first_name = forms.CharField(max_length=50, required=True,
                                 error_messages={'required': 'El nombre es obligatorio'})
    last_name = forms.CharField(max_length=50, required=True,
                                error_messages={'required': 'El apellido es obligatorio'})





class RegistroClienteFormulario(forms.Form):
    username = forms.CharField(max_length=50, required=True,
                               error_messages={'required': 'El nombre de usuario es obligatorio'})
    email = forms.EmailField(label='Correo electrónico', required=True,
                             error_messages={'required': 'El correo electrónico es obligatorio'})
    password = forms.CharField(widget=forms.PasswordInput, max_length=128, min_length=8, required=True,
                               error_messages={'required': 'La contraseña es obligatoria',
                                               'max_length': 'El campo nombre no puede ser tan largo.',
                                               'min_length': 'La contraseña tiene que contener 8 caracteres'})
    prefix_tel = forms.CharField(max_length=3, required=True,
                                 error_messages={'required': 'Seleccione un prefijo'})
    telefono = forms.CharField(max_length=10, required=True,
                               error_messages={'required': 'El teléfono es obligatorio'})
    first_name = forms.CharField(max_length=50, required=True,
                                 error_messages={'required': 'El nombre es obligatorio'})
    last_name = forms.CharField(max_length=50, required=True,
                                error_messages={'required': 'El apellido es obligatorio'})
    pais = forms.CharField(max_length=50, required=True,
                           error_messages={'required': 'El país es obligatorio'})
    ciudad = forms.CharField(max_length=50, required=True,
                             error_messages={'required': 'La ciudad es obligatoria'})
    codigo_postal = forms.CharField(max_length=10, required=True,
                                    error_messages={'required': 'El código postal es obligatorio'})
    direcion = forms.CharField(max_length=100, required=True,
                               error_messages={'required': 'La dirección es obligatoria'})
    numero = forms.CharField(max_length=10, required=True,
                             error_messages={'required': 'El número de calle es obligatorio'})
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': "El nombre de usuario ya existe"})


class RestauranteForm(forms.Form):
    nombre_restaurante = forms.CharField( max_length=100, required=True,
                           error_messages={'required': 'Es obligatorio añadir un nombre al restaurante'})
    pais = forms.CharField(max_length=50, required=True,
                           error_messages={'required': 'El país es obligatorio'})
    ciudad = forms.CharField(max_length=50, required=True,
                             error_messages={'required': 'La ciudad es obligatoria'})
    codigo_postal = forms.CharField(max_length=10, required=True,
                                    error_messages={'required': 'El código postal es obligatorio'})
    direcion = forms.CharField(max_length=100, required=True,
                               error_messages={'required': 'La dirección es obligatoria'})
    numero = forms.CharField(max_length=10, required=True,
                             error_messages={'required': 'El número de calle es obligatorio'})

    descripcion = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe la descripción que desees aquí...'}),required=True,
                           error_messages={'required': 'És obligatori afegir una descripció mínima al restaurant.'})


    imagenes = forms.ClearableFileInput(attrs={"allow_multiple_selected": True} )

class AddPlatoFormulario(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'El nombre del plato es obligatorio.'}
    )
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        min_value=0.01,
        error_messages={
            'required': 'El precio del plato es obligatorio.',
            'min_value': 'El precio debe ser un valor positivo mayor a cero.'
        }
    )
    descuento = forms.DecimalField(
        max_digits=3,
        decimal_places=0,
        required=False,
        min_value=0,
        max_value=100,
        error_messages={
            'min_value': 'El descuento no puede ser menor que 0.',
            'max_value': 'El descuento no puede ser mayor que 100.'
        }
    )



