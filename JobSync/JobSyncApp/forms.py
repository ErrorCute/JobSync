from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import CustomUser, Comuna, Trabajo
import re
from django.core.exceptions import ValidationError
from datetime import datetime, time
from django.utils.timezone import make_aware
class UsuarioUserForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    apellido = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    telefono = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    repetir_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}))
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), widget=forms.Select(attrs={'placeholder': 'Comuna'}))

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{9}$', telefono):
            raise forms.ValidationError("El teléfono debe contener  9 digitos.")
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        repetir_contraseña = cleaned_data.get("repetir_contraseña")

        if contraseña and len(contraseña) < 5:
            raise forms.ValidationError("La contraseña debe tener más de 4 caracteres.")
        
        if contraseña != repetir_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")

    def save(self):
        usuario = CustomUser.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['nombre'],
            last_name=self.cleaned_data['apellido'],
            telefono=self.cleaned_data['telefono'],
            comuna=self.cleaned_data['comuna'],
            password=self.cleaned_data['contraseña']
        )
        usuario.save()
        return usuario

class ModificarUsuarioForm(forms.ModelForm):
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), required=False)
    repetir_contraseña = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'}), required=False)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), widget=forms.Select(attrs={'placeholder': 'Comuna'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'telefono', 'comuna']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'comuna': forms.Select(attrs={'placeholder': 'Comuna'}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{9}$', telefono):
            raise forms.ValidationError("El teléfono debe contener  9 digitos.")
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        repetir_contraseña = cleaned_data.get("repetir_contraseña")
        email = cleaned_data.get("email")

        if contraseña and len(contraseña) < 5:
            raise forms.ValidationError("La contraseña debe tener más de 4 caracteres.")
       
    
        if contraseña or repetir_contraseña:
            if contraseña != repetir_contraseña:
                raise forms.ValidationError("Las contraseñas no coinciden.")

        cleaned_data["username"] = email

        return cleaned_data

    def save(self, commit=True):
        self.instance.username = self.cleaned_data['email']
        self.instance.comuna = self.cleaned_data.get('comuna', self.instance.comuna)
        return super(ModificarUsuarioForm, self).save(commit)

class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ['nombre_trabajo', 'nombre_titular', 'rut_titular', 'telefono', 'comuna', 'direccion', 'fecha', 'hora_inicio', 'hora_termino', 'valor']
        widgets = {
            'nombre_trabajo': forms.TextInput(attrs={'placeholder': 'Nombre del trabajo'}),
            'nombre_titular': forms.TextInput(attrs={'placeholder': 'Nombre del titular'}),
            'rut_titular': forms.TextInput(attrs={'placeholder': 'RUT del titular'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'comuna': forms.Select(attrs={'placeholder': 'Comuna'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha (YYYY-MM-DD)'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de inicio (HH:MM)'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de término (HH:MM)'}),
            'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < datetime.now().date():
            raise ValidationError("La fecha no puede ser anterior a la fecha actual")
        return fecha
   
    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data['hora_inicio']
        hora_minima = time(8, 0)  # Hora mínima: 8:00 AM
        hora_maxima = time(19, 0)  # Hora máxima: 7:00 PM
        if hora_inicio < hora_minima or hora_inicio > hora_maxima:
            raise ValidationError("La hora de inicio debe estar entre las 8:00 AM y las 7:00 PM")
        return hora_inicio

    def clean_hora_termino(self):
        hora_termino = self.cleaned_data['hora_termino']
        hora_minima = time(8, 0)  # Hora mínima: 8:00 AM
        hora_maxima = time(19, 0)  # Hora máxima: 7:00 PM
        if hora_termino < hora_minima or hora_termino > hora_maxima:
            raise ValidationError("La hora de término debe estar entre las 8:00 AM y las 7:00 PM")
        hora_inicio = self.cleaned_data.get('hora_inicio')
        if hora_inicio and hora_termino and hora_termino <= hora_inicio:
            raise ValidationError("La hora de término debe ser mayor que la hora de inicio.")
        return hora_termino
    
    def clean_rut_titular(self):
        rut_titular = self.cleaned_data.get('rut_titular')
        if len(rut_titular) < 11:
            raise forms.ValidationError("El RUT es incorrecto")
        if not re.match(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$', rut_titular):
            raise forms.ValidationError("El RUT debe estar en el formato 12.345.678-9.")
        return rut_titular

class ModificarTrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ['nombre_trabajo', 'nombre_titular', 'rut_titular', 'telefono', 'comuna', 'direccion', 'fecha', 'hora_inicio', 'hora_termino', 'valor']
        widgets = {
            'nombre_trabajo': forms.TextInput(attrs={'placeholder': 'Nombre del trabajo'}),
            'nombre_titular': forms.TextInput(attrs={'placeholder': 'Nombre del titular'}),
            'rut_titular': forms.TextInput(attrs={'placeholder': 'RUT del titular'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'comuna': forms.Select(attrs={'placeholder': 'Comuna'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha (YYYY-MM-DD)'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de inicio (HH:MM)'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de término (HH:MM)'}),
            'valor': forms.NumberInput(attrs={'placeholder': 'Valor'}),
        }

    
    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data['hora_inicio']
        hora_minima = time(8, 0)  # Hora mínima: 8:00 AM
        hora_maxima = time(19, 0)  # Hora máxima: 7:00 PM
        if hora_inicio < hora_minima or hora_inicio > hora_maxima:
            raise ValidationError("La hora de inicio debe estar entre las 8:00 AM y las 7:00 PM")
        return hora_inicio

    def clean_hora_termino(self):
        hora_termino = self.cleaned_data['hora_termino']
        hora_minima = time(8, 0)  # Hora mínima: 8:00 AM
        hora_maxima = time(19, 0)  # Hora máxima: 7:00 PM
        if hora_termino < hora_minima or hora_termino > hora_maxima:
            raise ValidationError("La hora de término debe estar entre las 8:00 AM y las 7:00 PM")
        hora_inicio = self.cleaned_data.get('hora_inicio')
        if hora_inicio and hora_termino and hora_termino <= hora_inicio:
            raise ValidationError("La hora de término debe ser mayor que la hora de inicio.")
        return hora_termino

    def clean_rut_titular(self):
        rut_titular = self.cleaned_data.get('rut_titular')
        if len(rut_titular) < 11:
            raise forms.ValidationError("El RUT es incorrecto.")
        if not re.match(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$', rut_titular):
            raise forms.ValidationError("El RUT debe estar en el formato 12.345.678-9.")
        return rut_titular


class RutForm(forms.Form):
    rut_titular = forms.CharField(max_length=12, label='RUT del titular')

    def clean_rut_titular(self):
        rut_titular = self.cleaned_data.get('rut_titular')
        if len(rut_titular) < 11:
            raise forms.ValidationError("El RUT es incorrecto.")
        if not re.match(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$', rut_titular):
            raise forms.ValidationError("El RUT debe estar en el formato 12.345.678-9.")
        return rut_titular


class ReagendarTrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ['fecha', 'hora_inicio', 'hora_termino']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha (YYYY-MM-DD)'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de inicio (HH:MM)'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Hora de término (HH:MM)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_termino = cleaned_data.get('hora_termino')

        if not fecha or not hora_inicio or not hora_termino:
            return cleaned_data

        # Convertir fecha y horas a datetime para comparaciones
        fecha_inicio = make_aware(datetime.combine(fecha, hora_inicio))
        fecha_termino = make_aware(datetime.combine(fecha, hora_termino))

        # Obtener otros trabajos del colaborador en esa fecha
        trabajos = Trabajo.objects.filter(
            colaborador=self.instance.colaborador,
            fecha=fecha
        ).exclude(id=self.instance.id)

        for trabajo in trabajos:
            trabajo_inicio = make_aware(datetime.combine(trabajo.fecha, trabajo.hora_inicio))
            trabajo_termino = make_aware(datetime.combine(trabajo.fecha, trabajo.hora_termino))

            # Comprobar si hay solapamiento
            if (fecha_inicio < trabajo_termino) and (fecha_termino > trabajo_inicio):
                raise ValidationError("Ya tienes un trabajo asignado en ese horario.")

        return cleaned_data

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < self.instance.fecha:
            raise ValidationError("La fecha no puede ser anterior a la fecha original del trabajo.")
        return fecha

    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data['hora_inicio']
        hora_minima = time(8, 0)  # Hora mínima: 8:00 AM
        hora_maxima = time(19, 0)  # Hora máxima: 7:00 PM
        if hora_inicio < hora_minima or hora_inicio > hora_maxima:
            raise ValidationError("La hora de inicio debe estar entre las 8:00 AM y las 7:00 PM")
        return hora_inicio

    def clean_hora_termino(self):
        hora_termino = self.cleaned_data['hora_termino']
        hora_minima = time(8, 0)  # Hora mínima: 8:00 AM
        hora_maxima = time(19, 0)  # Hora máxima: 7:00 PM
        if hora_termino < hora_minima or hora_termino > hora_maxima:
            raise ValidationError("La hora de término debe estar entre las 8:00 AM y las 7:00 PM")
        hora_inicio = self.cleaned_data.get('hora_inicio')
        if hora_inicio and hora_termino and hora_termino <= hora_inicio:
            raise ValidationError("La hora de término debe ser mayor que la hora de inicio.")
        return hora_termino