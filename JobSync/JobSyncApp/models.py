
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

# class Trabajo(models.Model):
#     usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     nombre_trabajo = models.CharField(max_length=100)
#     nombre_titular = models.CharField(max_length=100)
#     rut_titular = models.CharField(max_length=20)
#     comuna_titular = models.CharField(max_length=100)
#     direccion  = models.CharField(max_length=200)
#     fecha = models.DateField()
#     hora = models.TimeField()
#     valor = models.IntegerField(default=0)
#     estado = models.CharField(max_length=20, default='Pendiente')

#     def __str__(self):
#         return self.nombre_trabajo