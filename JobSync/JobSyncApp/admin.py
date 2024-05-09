from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefono', 'is_active', 'is_staff', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
