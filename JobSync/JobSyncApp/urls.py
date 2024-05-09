from django.urls import path
from .import views


urlpatterns = [

    path('index', views.index, name='index'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    
    path('', views.custom_login, name='custom_login'),
    path('registro/', views.registro, name='registro'), 

    path('custom_logout/', views.custom_logout, name='custom_logout'),

    # admin ---- 
    path('home/', views.home, name='home'), 

    # colaborador ---
    path('index_colaborador/', views.index_colaborador, name='index_colaborador'),
]