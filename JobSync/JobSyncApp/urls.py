from django.urls import path
from .import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('', views.custom_login, name='custom_login'),
    path('registro/', views.registro, name='registro'), 
    path('home/', views.home, name='home'), 
    path('custom_logout/', views.custom_logout, name='custom_logout'),
]