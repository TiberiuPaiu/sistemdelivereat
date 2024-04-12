from django import forms

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
