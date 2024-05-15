
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser  # Cambia el nombre de la función login
from .forms import  UsuarioUserForm,RegistroForm
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
                if user.rol:
                    return redirect('index_colaborador')
                else:
                    return redirect('home') 
    else:
        formulario = UsuarioUserForm()    
        
    return render(request, 'registration/login.html', {'formulario': formulario})


def index(request):
    return render(request,'index.html')

def custom_logout(request):
    logout(request)
  
    return redirect('/')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario y crear un nuevo usuario
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            contraseña = form.cleaned_data['contraseña']
            repetir_contraseña = form.cleaned_data['repetir_contraseña']

            # Verificar si el usuario ya existe
            if not CustomUser.objects.filter(email=email).exists():
                # Crear el usuario si no existe
                nuevo_usuario = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    first_name=nombre,
                    last_name=apellido,
                    telefono=telefono,
                    password=contraseña
                )
                # Puedes guardar cualquier otro campo personalizado aquí si es necesario
              
                nuevo_usuario.save()
                return redirect('home')  # Redirigir a una página de éxito
            else:
                # El usuario ya existe, mostrar un mensaje de error
                mensaje_error = "Ya existe un usuario con este correo electrónico"
                return render(request, 'registro.html', {'form': form, 'error_message': mensaje_error})
    else:
        form = RegistroForm() 
        return render(request, 'registro.html',{'form': form})


def lista_colaboradores(request ):
    colaboradores = CustomUser.objects.filter(rol=True)
    return render(request, 'admin/colaboradores.html', {'colaboradores': colaboradores})

def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return redirect('colaboradores')  # Redirige a la página de la lista de usuarios después de eliminar
    else:
        return render(request, 'admin/eliminar_usuario.html', {'user_id': user_id})


def home(request):
    return render(request, 'home.html')

def index_colaborador(request):
    return render(request ,'colaborador/index_colaborador.html')

@login_required
def sobre_nosotros(request):
    return render(request, 'sobrenosotros.html')