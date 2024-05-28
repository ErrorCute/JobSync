from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Comuna, Trabajo, Agenda
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefono', 'is_active', 'is_staff', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Trabajo)
admin.site.register(Agenda)

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ['nombre'] 
# Register your models here.
