
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  # Cambia el nombre de la función login
from .forms import UsuarioUserForm
from django.contrib.auth.decorators import login_required

def custom_login(request):
    if request.method == 'POST':
        formulario = UsuarioUserForm(data=request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data.get('username')  
            password = formulario.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)  
            if user is not None:
                login(request, user) 
                return redirect('sobre_nosotros') 
    else:
        formulario = UsuarioUserForm()    
        
    return render(request, 'registration/login.html', {'formulario': formulario})



def index(request):
    return render(request,'index.html')


def registro(request):
    return render(request, 'registro.html')

@login_required

def sobre_nosotros(request):
    return render(request, 'sobrenosotros.html')