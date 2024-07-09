# decorators.py
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol.nombre != 'Admin':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def colaborador_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol.nombre != 'Colaborador':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
