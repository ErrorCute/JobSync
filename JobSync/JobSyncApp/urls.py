from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('login/', views.custom_login, name='custom_login'), 
]