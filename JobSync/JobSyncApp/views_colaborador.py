
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser,Trabajo

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
