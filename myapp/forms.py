from django import forms

class RegistroFormulario(forms.Form):
    nombre_negocio =forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    prefix_tel = forms.CharField(max_length=5)
    telefono = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)




