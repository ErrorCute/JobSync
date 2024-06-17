
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Trabajo

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
    selected_month_name = None
    if selected_month:
        for month in months:
            if month['value'] == selected_month:
                selected_month_name = month['name']
                break

    usuarios = CustomUser.objects.filter(rol=True)
    trabajos = Trabajo.objects.filter(estado='completado')

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