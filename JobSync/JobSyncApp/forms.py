from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import CustomUser  # Importa tu modelo de usuario personalizado

class UsuarioUserForm(AuthenticationForm):
    class Meta:
        model = CustomUser  # Utiliza tu modelo de usuario personalizado en lugar de User
        fields = ['username', 'password']  # Ajusta los campos según tu modelo

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    apellido = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    telefono = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    repetir_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}))


    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        repetir_contraseña = cleaned_data.get("repetir_contraseña")

        if contraseña != repetir_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden")

    def save(self):
        # Crea una instancia de CustomUser y guarda los datos del formulario en ella
        usuario = CustomUser.objects.create_user(
            username=self.cleaned_data['email'],  # Utiliza el email como nombre de usuario
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['nombre'],
            last_name=self.cleaned_data['apellido'],
            telefono=self.cleaned_data['telefono'],
            password=self.cleaned_data['contraseña']
        )
        usuario.save()
        return usuario
    

class ModificarUsuarioForm(forms.ModelForm):
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), required=False)
    repetir_contraseña = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        }

    def __init__(self, *args, **kwargs):
        super(ModificarUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False  # Permitir editar el username

    # Sobreescribir clean_username para asegurarse de que el username no esté duplicado
    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso")
        return username

    # Validación de contraseña y repetir contraseña
    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        repetir_contraseña = cleaned_data.get("repetir_contraseña")

        # Verificar si se ingresó al menos una contraseña
        if contraseña or repetir_contraseña:
            # Verificar si ambas contraseñas coinciden
            if contraseña != repetir_contraseña:
                raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data