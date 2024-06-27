
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Trabajo,Estado

from datetime import datetime


def reporte_general(request):
    # Obtener el mes seleccionado de los parámetros GET
    selected_month = request.GET.get('month')
    
    # Lista de meses para el select
    months = [
        {'value': '01', 'name': 'Enero'},
        {'value': '02', 'name': 'Febrero'},
        {'value': '03', 'name': 'Marzo'},
        {'value': '04', 'name': 'Abril'},
        {'value': '05', 'name': 'Mayo'},
        {'value': '06', 'name': 'Junio'},
        {'value': '07', 'name': 'Julio'},
        {'value': '08', 'name': 'Agosto'},
        {'value': '09', 'name': 'Septiembre'},
        {'value': '10', 'name': 'Octubre'},
        {'value': '11', 'name': 'Noviembre'},
        {'value': '12', 'name': 'Diciembre'},
    ]

    # Obtener el nombre del mes seleccionado
    current_month = datetime.now().strftime('%m')
    selected_month_name = None

    # Si no se selecciona ningún mes, seleccionar el mes actual
    if not selected_month:
        selected_month = current_month

    for month in months:
        if month['value'] == selected_month:
            selected_month_name = month['name']
            break

    usuarios = CustomUser.objects.filter(rol=True)
    estado_completado = Estado.objects.get(nombre='completado')
    trabajos = Trabajo.objects.filter(estado=estado_completado)

    # Filtrar trabajos por el mes seleccionado
    if selected_month:
        trabajos = trabajos.filter(fecha__month=selected_month)

    total_trabajos = trabajos.count()
    total_recaudado = sum(trabajo.valor for trabajo in trabajos)

    usuarios_data = []
    for usuario in usuarios:
        trabajos_usuario = trabajos.filter(colaborador=usuario)
        total_trabajos_usuario = trabajos_usuario.count()
        total_recaudado_usuario = sum(trabajo.valor for trabajo in trabajos_usuario)
        usuarios_data.append({
            'username':  f"{usuario.last_name} {usuario.first_name}",
            'total_trabajos': total_trabajos_usuario,
            'total_recaudado': total_recaudado_usuario
        })

    context = {
        'usuarios_data': usuarios_data,
        'total_trabajos': total_trabajos,
        'total_recaudado': total_recaudado,
        'months': months,
        'selected_month': selected_month,
        'selected_month_name': selected_month_name,
    }

    return render(request, 'admin/reportes/reporte_general.html', context)


def index_reporte(request):
    return render(request,'admin/reportes/index_reporte.html')

def selecciona_colaborador_reporte(request):
    colaboradores = CustomUser.objects.filter(rol=True)
    return render (request,'admin/reportes/selecciona_colaborador_reporte.html',{'colaboradores': colaboradores})


def reporte_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(CustomUser, id=colaborador_id)
    
    # Obtener la fecha seleccionada de los parámetros GET
    selected_month = request.GET.get('month')
    
    # Lista de meses para el select
    months = [
        {'value': '01', 'name': 'Enero'},
        {'value': '02', 'name': 'Febrero'},
        {'value': '03', 'name': 'Marzo'},
        {'value': '04', 'name': 'Abril'},
        {'value': '05', 'name': 'Mayo'},
        {'value': '06', 'name': 'Junio'},
        {'value': '07', 'name': 'Julio'},
        {'value': '08', 'name': 'Agosto'},
        {'value': '09', 'name': 'Septiembre'},
        {'value': '10', 'name': 'Octubre'},
        {'value': '11', 'name': 'Noviembre'},
        {'value': '12', 'name': 'Diciembre'},
    ]

    # Obtener el nombre del mes seleccionado
    current_month = datetime.now().strftime('%m')
    
    selected_month_name = None 
    # Si no se selecciona ningún mes, seleccionar el mes actual
    if not selected_month:
        selected_month = current_month

    for month in months:
        if month['value'] == selected_month:
            selected_month_name = month['name']
            break
    
    estado_completado = Estado.objects.get(nombre='completado')

    # Obtener trabajos completados del colaborador
    trabajos_completados = Trabajo.objects.filter(colaborador=colaborador, estado=estado_completado)
    
    # Filtrar trabajos por el mes seleccionado si está definido
    if selected_month:
        trabajos_completados = trabajos_completados.filter(fecha__month=selected_month)

    # Crear una lista para almacenar los detalles de los trabajos completados
    detalles_trabajos = []
    for trabajo in trabajos_completados:
        detalle_trabajo = {
            'nombre': trabajo.nombre_trabajo,
            'fecha_realizado': trabajo.fecha,
            'valor': trabajo.valor,
            # Añadir más detalles según sea necesario
        }
        detalles_trabajos.append(detalle_trabajo)
    
    # Contar el número total de trabajos completados
    total_trabajos = len(trabajos_completados)
    
    # Calcular el total recaudado por el colaborador
    total_recaudado = sum(trabajo.valor for trabajo in trabajos_completados)
    
    context = {
        'colaborador': colaborador,
        'trabajos_completados': total_trabajos,
        'total_recaudado': total_recaudado,
        'detalles_trabajos': detalles_trabajos,  # Agregar los detalles de los trabajos
        'selected_month': selected_month,
        'selected_month_name': selected_month_name,
        'months': months,
    }

    return render(request, 'admin/reportes/reporte_colaborador.html', context)



def mi_reporte(request):
    colaborador = request.user  # Obtener el usuario logueado como colaborador
    
    # Obtener la fecha seleccionada de los parámetros GET
    selected_month = request.GET.get('month')
    
    # Lista de meses para el select
    months = [
        {'value': '01', 'name': 'Enero'},
        {'value': '02', 'name': 'Febrero'},
        {'value': '03', 'name': 'Marzo'},
        {'value': '04', 'name': 'Abril'},
        {'value': '05', 'name': 'Mayo'},
        {'value': '06', 'name': 'Junio'},
        {'value': '07', 'name': 'Julio'},
        {'value': '08', 'name': 'Agosto'},
        {'value': '09', 'name': 'Septiembre'},
        {'value': '10', 'name': 'Octubre'},
        {'value': '11', 'name': 'Noviembre'},
        {'value': '12', 'name': 'Diciembre'},
    ]

    # Obtener el nombre del mes seleccionado
    current_month = datetime.now().strftime('%m')
    
    selected_month_name = None
    
    # Si no se selecciona ningún mes, seleccionar el mes actual
    if not selected_month:
        selected_month = current_month
    
    # Buscar el nombre del mes seleccionado en la lista de meses
    for month in months:
        if month['value'] == selected_month:
            selected_month_name = month['name']
            break
    
    estado_completado = Estado.objects.get(nombre='completado')
    # Obtener trabajos completados del colaborador
    trabajos_completados = Trabajo.objects.filter(colaborador=colaborador, estado=estado_completado)
    
    # Filtrar trabajos por el mes seleccionado si está definido
    if selected_month:
        trabajos_completados = trabajos_completados.filter(fecha__month=selected_month)

    # Crear una lista para almacenar los detalles de los trabajos completados
    detalles_trabajos = []
    for trabajo in trabajos_completados:
        detalle_trabajo = {
            'nombre': trabajo.nombre_trabajo,
            'fecha_realizado': trabajo.fecha,
            'valor': trabajo.valor,
            # Añadir más detalles según sea necesario
        }
        detalles_trabajos.append(detalle_trabajo)
    
    # Contar el número total de trabajos completados
    total_trabajos = len(trabajos_completados)
    
    # Calcular el total recaudado por el colaborador
    total_recaudado = sum(trabajo.valor for trabajo in trabajos_completados)
    
    context = {
        'colaborador': colaborador,
        'trabajos_completados': total_trabajos,
        'total_recaudado': total_recaudado,
        'detalles_trabajos': detalles_trabajos,  # Agregar los detalles de los trabajos
        'selected_month': selected_month,
        'selected_month_name': selected_month_name,
        'months': months,
    }

    return render(request, 'colaborador/mi_reporte.html', context)

