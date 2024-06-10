import locale
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Trabajo
from django.contrib import messages
from datetime import datetime
from babel.dates import format_date, parse_date
from .forms import ReagendarTrabajoForm
@login_required
def mi_agenda(request):
    # Asegúrate de que request.user es una instancia de CustomUser
    if not isinstance(request.user, CustomUser):
        raise ValueError("El usuario autenticado no es una instancia de CustomUser.")
    
    colaborador = request.user
    return render(request, 'colaborador/agenda/mi_agenda.html', {'colaborador': colaborador})




def mi_trabajos(request, colaborador_id, fecha):
    colaborador = get_object_or_404(CustomUser, id=colaborador_id)
    trabajos = Trabajo.objects.filter(fecha=fecha, colaborador_id=colaborador_id)
    
    # Establecer la configuración local a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Formatear la fecha
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
    fecha_formateada = format_date(fecha_obj, format="full", locale="es")

    context = {
        'colaborador': colaborador,
        'trabajos': trabajos,
        'fecha': fecha_formateada
    }
    return render(request, 'colaborador/agenda/mi_trabajos.html', context)

def actualizar_estado_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    if request.method == 'POST':
        rut_titular = request.POST.get('rut_titular')
        if trabajo.rut_titular == rut_titular:
            trabajo.estado = 'completado'
            trabajo.save()
            messages.success(request, 'Estado del trabajo actualizado con éxito')
        else:
            messages.error(request, 'El RUT no coincide con el titular del trabajo')
        
        return redirect('mi_trabajos', colaborador_id=trabajo.colaborador.id, fecha=trabajo.fecha)

    return render(request, 'colaborador/agenda/mi_trabajos.html', {'trabajo': trabajo})

def reagendar_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    if request.method == 'POST':
        form = ReagendarTrabajoForm(request.POST, instance=trabajo)
        if form.is_valid():
            form.save()
            trabajo.reagendado_contador += 1
            trabajo.estado = 'reagendado'
            trabajo.save()
            return redirect('mi_trabajos', colaborador_id=trabajo.colaborador.id, fecha=trabajo.fecha)
    else:
        form = ReagendarTrabajoForm(instance=trabajo)
    return render(request, 'colaborador/agenda/reagendar_trabajo.html', {'form': form, 'trabajo': trabajo})