
# Create your models here
from django.contrib.auth.models import AbstractUser
from django.db import models

class Comuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    telefono = models.CharField(max_length=15)
    ROL_CHOICES = [
        (True, 'Colaborador'),
        (False, 'Admin'),
    ]
    
    rol = models.BooleanField(choices=ROL_CHOICES, default=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, blank=True)  

class Trabajo(models.Model):
    colaborador = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_trabajo = models.CharField(max_length=100)
    nombre_titular = models.CharField(max_length=100)
    rut_titular = models.CharField(max_length=12)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=255)
    fecha = models.DateField()
    hora = models.TimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    ESTADO_CHOICES = [
        ('sin_asignar', 'Sin asignar'),
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='sin_asignar')

    def __str__(self):
        return self.nombre_trabajo
    

class Agenda(models.Model):
    colaborador = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trabajos = models.ManyToManyField(Trabajo)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Agenda de {self.colaborador.username}"