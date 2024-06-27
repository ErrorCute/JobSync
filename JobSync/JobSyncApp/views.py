# views.py

import locale
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Comuna, Trabajo,Rol, Empresa
from .forms import ModificarTrabajoForm, UsuarioUserForm, RegistroForm, ModificarUsuarioForm, TrabajoForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from django.utils.dateformat import DateFormat
from babel.dates import format_date, parse_date
from django.contrib import messages
from .decorators import user_is_colaborador, user_is_admin

def custom_login(request):
    if request.method == 'POST':
        formulario = UsuarioUserForm(data=request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data.get('username')
            password = formulario.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_deleted:  # Verifica si el usuario está eliminado
                    # Obtener el subdominio de la solicitud
                    subdominio = request.get_host().split('.')[0]
                    try:
                        empresa = Empresa.objects.get(subdominio=subdominio)
                        if user.empresa == empresa:
                            login(request, user)
                            if user.rol.nombre == 'Admin':
                                return redirect('home')  # Página de inicio para Admin
                            elif user.rol.nombre == 'Colaborador':
                                return redirect('index_colaborador')  # Página de inicio para Colaborador
                            else:
                                messages.error(request, 'Rol de usuario no reconocido.')
                        else:
                            messages.error(request, 'El usuario no pertenece a esta empresa.')
                    except Empresa.DoesNotExist:
                        messages.error(request, 'Empresa no encontrada.')
                else:
                    messages.error(request, 'Este usuario ha sido eliminado.')
            else:
                messages.error(request, 'Credenciales no válidas.')
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
            comuna = form.cleaned_data['comuna']  

            # Verificar si el usuario ya existe
            if not CustomUser.objects.filter(email=email).exists():
                # Crear el usuario si no existe
                nuevo_usuario = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    first_name=nombre,
                    last_name=apellido,
                    telefono=telefono,
                    comuna=comuna,  
                    password=contraseña
                )
                rol_colaborador = Rol.objects.get(nombre='Colaborador')

                nuevo_usuario.rol = rol_colaborador 
                nuevo_usuario.save()
                return redirect('colaboradores') 
            else:
                # El usuario ya existe, mostrar un mensaje de error
                mensaje_error = "Ya existe un usuario con este correo electrónico"
                return render(request, 'registro.html', {'form': form, 'error_message': mensaje_error})
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required

def lista_colaboradores(request):
    colaboradores = CustomUser.objects.filter(empresa=request.empresa)
    return render(request, 'admin/colaboradores.html', {'colaboradores': colaboradores})

@login_required
@user_is_admin
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return redirect('colaboradores')
    else:
        return render(request, 'admin/eliminar_usuario.html', {'user_id': user_id})

@login_required
@user_is_admin
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

@login_required

def home(request):
    return render(request, 'home.html')

@login_required
@user_is_colaborador
def index_colaborador(request):
    return render(request ,'colaborador/index_colaborador.html')

@login_required
def sobre_nosotros(request):
    return render(request, 'sobrenosotros.html')

# ------------------------------------------------ gestion de trabajos como administrador ----------------------

@login_required
@user_is_admin
def index_trabajo(request):
    return render (request,'admin/gestion_trabajos/trabajos/index_trabajo.html')

@login_required
@user_is_admin
def trabajos(request):
    comuna = Comuna.objects.all()
    trabajos = Trabajo.objects.filter(empresa=request.empresa)
    return render(request, 'admin/gestion_trabajos/trabajos/trabajos.html', {'trabajos': trabajos,'comuna':comuna})

@login_required
@user_is_admin
def crear_trabajo(request):
    if request.method == 'POST':
        form = TrabajoForm(request.POST)
        if form.is_valid():
            trabajo = form.save(commit=False)
            trabajo.save()
            return redirect('trabajos')  
    else:
        form = TrabajoForm()
    return render(request, 'admin/gestion_trabajos/trabajos/crear_trabajo.html', {'form': form})

@login_required
@user_is_admin
def modificar_trabajo(request, trabajo_id):
    trabajo = Trabajo.objects.get(id=trabajo_id)
    if request.method == 'POST':
        form = ModificarTrabajoForm(request.POST, instance=trabajo)
        if form.is_valid():
            form.save()
            return redirect('trabajos')  
    else:
        form = ModificarTrabajoForm(instance=trabajo)
    return render(request, 'admin/gestion_trabajos/trabajos/modificar_trabajo.html', {'form': form})

@login_required
@user_is_admin
def eliminar_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    trabajo.delete()  # Esto llamará al método delete personalizado
    return redirect('trabajos')

@login_required
@user_is_admin
def seleccionar_colaborador(request):
    colaboradores = CustomUser.objects.filter(rol=True)
    return render(request, 'admin/gestion_trabajos/Asignar_trabajos/seleccionar_colaborador.html', {'colaboradores': colaboradores})

from django.utils.dateformat import DateFormat

@login_required
@user_is_admin
def ver_agenda(request, colaborador_id):
    colaborador = get_object_or_404(CustomUser, id=colaborador_id)
    trabajos = Trabajo.objects.filter(
        colaborador=colaborador,
        estado__in=['pendiente', 'reagendado']
    )
    
    eventos = [
        {
            'title': trabajo.nombre_trabajo,
            'start': DateFormat(trabajo.fecha).format('Y-m-d'),
            'description': trabajo.nombre_titular,
        } for trabajo in trabajos
    ]
    
    return render(request, 'admin/gestion_trabajos/Asignar_trabajos/ver_agenda.html', {
        'colaborador': colaborador,
        'eventos': eventos,
    })

@login_required
@user_is_admin
def trabajos_sin_asignar(request, colaborador_id, fecha):
    colaborador = get_object_or_404(CustomUser, id=colaborador_id)
    trabajos_sin_asignar = Trabajo.objects.filter(fecha=fecha, colaborador__isnull=True)
    trabajos_asignados = Trabajo.objects.filter(fecha=fecha, colaborador=colaborador)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Formatear la fecha
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
    fecha_formateada = format_date(fecha_obj, format="full", locale="es")

    context = {
        'colaborador': colaborador,
        'trabajos_sin_asignar': trabajos_sin_asignar,
        'trabajos_asignados': trabajos_asignados,
        'fecha': fecha_formateada
    }

    return render(request, 'admin/gestion_trabajos/Asignar_trabajos/trabajos_sin_asignar.html', context)

@login_required
@user_is_admin
def asignar_y_desasignar_trabajos(request, user_id):
    colaborador = get_object_or_404(CustomUser, id=user_id)
    trabajos_ids = request.POST.get('trabajos', '').split(',')
    trabajos_desasignar_ids = request.POST.get('trabajos_desasignar', '').split(',')
    
    trabajos_ids = [trabajo_id for trabajo_id in trabajos_ids if trabajo_id]
    trabajos_desasignar_ids = [trabajo_id for trabajo_id in trabajos_desasignar_ids if trabajo_id]

    trabajos_a_asignar = Trabajo.objects.filter(id__in=trabajos_ids)
    trabajos_a_desasignar = Trabajo.objects.filter(id__in=trabajos_desasignar_ids)

    # Validación de solapamiento de horarios
    for trabajo1 in trabajos_a_asignar:
        for trabajo2 in trabajos_a_asignar:
            if trabajo1.id != trabajo2.id:
                if (trabajo1.fecha == trabajo2.fecha) and \
                   (trabajo1.hora_inicio < trabajo2.hora_termino) and \
                   (trabajo1.hora_termino > trabajo2.hora_inicio):
                    messages.error(request, f"Los trabajos '{trabajo1.nombre_trabajo}' y '{trabajo2.nombre_trabajo}' coinciden en el rango horario.")
                    return redirect(request.META.get('HTTP_REFERER', 'admin/gestion_trabajos/Asignar_trabajos/trabajos_sin_asignar.html'))
    
    for trabajo in trabajos_a_asignar:
        trabajos_conflictivos = Trabajo.objects.filter(
            colaborador=colaborador, fecha=trabajo.fecha,
            hora_inicio__lt=trabajo.hora_termino, hora_termino__gt=trabajo.hora_inicio
        ).exclude(id=trabajo.id)
        
        if trabajos_conflictivos.exists():
            messages.error(request, f"Ya hay un trabajo asignado para este colaborador en este rango horario: {trabajo.nombre_trabajo}")
            return redirect(request.META.get('HTTP_REFERER', 'admin/gestion_trabajos/Asignar_trabajos/trabajos_sin_asignar.html'))

    # Asignar y desasignar trabajos
    for trabajo in trabajos_a_asignar:
        trabajo.colaborador = colaborador
        if trabajo.estado == 'sin_asignar':
            trabajo.estado = 'pendiente' if trabajo.reagendado_contador == 0 else 'reagendado'
        trabajo.save()

    for trabajo in trabajos_a_desasignar:
        trabajo.colaborador = None
        trabajo.estado = 'sin_asignar'
        trabajo.save()

    messages.success(request, "Cambios guardados con éxito.")
    return redirect(request.META.get('HTTP_REFERER', 'admin/gestion_trabajos/Asignar_trabajos/trabajos_sin_asignar.html'))
