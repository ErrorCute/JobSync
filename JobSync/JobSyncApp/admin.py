from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Comuna, Trabajo,Region,Rol,Empresa
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefono', 'is_active', 'is_staff', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Trabajo)


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ['nombre'] 
# Register your models here.

@admin.register(Region)    
class RegionAdmin(admin.ModelAdmin):
    list_display = ['nombre'] 
    
@admin.register(Rol)    
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre'] 

@admin.register(Empresa)    
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre','subdominio']     
# Register your models here.
