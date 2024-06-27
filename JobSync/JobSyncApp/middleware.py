from django.http import HttpResponseForbidden
from .models import Empresa

class EmpresaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split('.')[0]  # Obtener el dominio sin el puerto
        try:
            empresa = Empresa.objects.get(subdominio=host)
            request.empresa = empresa
            print(f"Subdominio: {host}, Empresa: {empresa.nombre}")  
        except Empresa.DoesNotExist:
            return HttpResponseForbidden("Empresa no encontrada")
        return self.get_response(request)
