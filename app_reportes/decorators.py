from functools import wraps
from django.shortcuts import redirect

def solo_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        usuario = getattr(request.user, 'usuario', None)

        if not usuario or not usuario.es_admin:
            return redirect('inicio')

        return view_func(request, *args, **kwargs)

    return _wrapped_view

def solo_usuario(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        usuario = getattr(request.user, 'usuario', None)

        if usuario and usuario.es_admin:
            return redirect('panel_admin')

        return view_func(request, *args, **kwargs)

    return _wrapped_view