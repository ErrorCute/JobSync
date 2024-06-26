from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Comuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Empresa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    subdominio = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

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
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomUserManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre_titular = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre_titular


class Estado(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre


class Trabajo(models.Model):
    colaborador = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre_trabajo = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True)
    reagendado_contador = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.nombre_trabajo


# Populating the Rol and Estado models with initial values

