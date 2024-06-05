
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser,Trabajo
from .forms import RutForm
from django.contrib import messages

@login_required
def mi_agenda(request):
    # Asegúrate de que request.user es una instancia de CustomUser
    if not isinstance(request.user, CustomUser):
        raise ValueError("El usuario autenticado no es una instancia de CustomUser.")
    
    colaborador = request.user
    return render(request, 'colaborador/agenda/mi_agenda.html', {'colaborador': colaborador})


from django.shortcuts import get_object_or_404

def mi_trabajos(request, colaborador_id, fecha):
    colaborador = get_object_or_404(CustomUser, id=colaborador_id)
    trabajos = Trabajo.objects.filter(fecha=fecha, colaborador_id=colaborador_id)
    return render(request, 'colaborador/agenda/mi_trabajos.html', {'trabajos': trabajos, 'fecha': fecha, 'colaborador': colaborador})

def actualizar_estado_trabajo(request, trabajo_id):
    trabajo = Trabajo.objects.get(id=trabajo_id)
    if request.method == 'POST':
        form = RutForm(request.POST)
        if form.is_valid():
            rut_titular = form.cleaned_data['rut_titular']
            if trabajo.rut_titular == rut_titular:
                trabajo.estado = 'completado'
                trabajo.save()
                messages.success(request, 'Estado del trabajo actualizado con éxito')
                return redirect('mi_trabajos', colaborador_id=trabajo.colaborador.id, fecha=trabajo.fecha)
            else:
                messages.error(request, 'El RUT no coincide con el titular del trabajo')
    else:
        form = RutForm()
    return render(request, 'colaborador/agenda/actualizar_estado_trabajo.html', {'form': form, 'trabajo': trabajo})