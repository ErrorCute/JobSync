
# Create your models here
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    telefono = models.CharField(max_length=15)
    ROL_CHOICES = [
        (True, 'Colaborador'),
        (False, 'Admin'),
    ]
    
    rol = models.BooleanField(choices=ROL_CHOICES, default=True)
