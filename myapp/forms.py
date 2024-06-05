from django import forms
from django.core.exceptions import ValidationError

from myapp.models import User


class RegistroFormulario(forms.Form):
    nombre_negocio =forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    prefix_tel = forms.CharField(max_length=5)
    telefono = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    archivos=forms.ClearableFileInput(attrs={"allow_multiple_selected": True})


class RestauranteForm(forms.Form):
    nombre_restaurante = forms.CharField( max_length=255)
    pais = forms.CharField(max_length=255)
    direcion = forms.CharField(max_length=255)
    ciudad = forms.CharField(max_length=255)
    numero = forms.IntegerField()
    codigo_postal = forms.CharField(max_length=255)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe la descripción que desees aquí...'}))
    imagenes = forms.ClearableFileInput(attrs={"allow_multiple_selected": True})



class AddUserFormulario(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    prefix_tel = forms.CharField(max_length=5)
    telefono = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)


class RegistroFormulario(forms.Form):
    nombre_negocio =forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    prefix_tel = forms.CharField(max_length=5)
    telefono = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    archivos=forms.ClearableFileInput(attrs={"allow_multiple_selected": True})



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




