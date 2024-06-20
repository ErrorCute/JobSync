
from django.core.exceptions import PermissionDenied

def user_is_colaborador(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.rol:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
