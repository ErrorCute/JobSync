# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
class Comuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo email debe ser establecido.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    telefono = models.CharField(max_length=15)  
    ROL_CHOICES = [
        (True, 'Colaborador'),
        (False, 'Admin'),
    ]
    rol = models.BooleanField(choices=ROL_CHOICES, default=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomUserManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class TrabajoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Trabajo(models.Model):
    colaborador = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_trabajo = models.CharField(max_length=100)
    nombre_titular = models.CharField(max_length=100)
    rut_titular = models.CharField(max_length=12)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=255)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    ESTADO_CHOICES = [
        ('sin_asignar', 'Sin asignar'),
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('reagendado', 'Reagendado'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='sin_asignar')
    reagendado_contador = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    objects = TrabajoManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.nombre_trabajo
