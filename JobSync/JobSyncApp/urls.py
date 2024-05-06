from django.urls import path
from .import views

urlpatterns = [
    path ('',views.login,name='login'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),

]