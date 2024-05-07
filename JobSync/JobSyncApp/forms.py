from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User
from django import forms

class UsuarioUserForm(AuthenticationForm):
    email = forms.EmailField(label="Correo electrónico")

class Meta:
        model = User
        fields = ['email', 'password']