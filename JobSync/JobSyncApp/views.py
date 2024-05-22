
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Comuna, Trabajo
from .forms import ModificarTrabajoForm, UsuarioUserForm, RegistroForm, ModificarUsuarioForm, TrabajoForm
from django.contrib.auth.decorators import login_required


def custom_login(request):
    if request.method == 'POST':
        formulario = UsuarioUserForm(data=request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data.get('username')  
            password = formulario.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
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
            comuna = form.cleaned_data['comuna']  # Obtener el campo 'comuna'

            # Verificar si el usuario ya existe
            if not CustomUser.objects.filter(email=email).exists():
                # Crear el usuario si no existe
                nuevo_usuario = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    first_name=nombre,
                    last_name=apellido,
                    telefono=telefono,
                    comuna=comuna,  # Asignar el campo 'comuna'
                    password=contraseña
                )
                nuevo_usuario.save()
                return redirect('colaboradores')  # Redirigir a una página de éxito
            else:
                # El usuario ya existe, mostrar un mensaje de error
                mensaje_error = "Ya existe un usuario con este correo electrónico"
                return render(request, 'registro.html', {'form': form, 'error_message': mensaje_error})
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def lista_colaboradores(request ):
    colaboradores = CustomUser.objects.filter(rol=True)
    return render(request, 'admin/colaboradores.html', {'colaboradores': colaboradores})

def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return redirect('colaboradores')  
    else:
        return render(request, 'admin/eliminar_usuario.html', {'user_id': user_id})

def modificar_usuario(request, user_id):
    usuario = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('colaboradores')
    else:
        form = ModificarUsuarioForm(instance=usuario)
    return render(request, 'admin/modificar_usuario.html', {'form': form, 'usuario_id': user_id})


def home(request):
    return render(request, 'home.html')

def index_colaborador(request):
    return render(request ,'colaborador/index_colaborador.html')

@login_required
def sobre_nosotros(request):
    return render(request, 'sobrenosotros.html')



# ------------------------------------------------ gestion de trabajos como administrador ----------------------

def index_trabajo(request):
    return render (request,'admin/gestion_trabajos/index_trabajo.html')

def trabajos(request):
    trabajos = Trabajo.objects.all()  # Obtener todos los trabajos
    return render(request, 'admin/gestion_trabajos/trabajos.html', {'trabajos': trabajos})


def crear_trabajo(request):

    if request.method == 'POST':
        form = TrabajoForm(request.POST)
        if form.is_valid():
            trabajo = form.save(commit=False)
            trabajo.save()
            return redirect('trabajos')  # Redirigir a la página de lista de trabajos
    else:
        form = TrabajoForm()
    return render(request, 'admin/gestion_trabajos/crear_trabajo.html', {'form': form})



def modificar_trabajo(request, trabajo_id):
    trabajo = Trabajo.objects.get(id=trabajo_id)
    if request.method == 'POST':
        form = ModificarTrabajoForm(request.POST, instance=trabajo)
        if form.is_valid():
            form.save()
            return redirect('trabajos')  # Redirige a donde sea necesario después de la modificación
    else:
        form = ModificarTrabajoForm(instance=trabajo)
    
    return render(request, 'admin/gestion_trabajos/modificar_trabajo.html', {'form': form})

def eliminar_trabajo(request, trabajo_id):
    trabajo= Trabajo.objects.get(id=trabajo_id)
    trabajo.delete()
    return redirect ('trabajos')