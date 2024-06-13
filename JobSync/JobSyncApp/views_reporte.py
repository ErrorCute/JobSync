
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Trabajo

def reporte_general(request):
    usuarios = CustomUser.objects.filter(rol=True)
    trabajos = Trabajo.objects.filter(estado='completado')
    
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
    }

    return render(request,'admin/reportes/reporte_general.html',context)