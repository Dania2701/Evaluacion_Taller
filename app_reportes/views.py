from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Reporte, Usuario
from .forms import ReporteForm, RegistroUsuarioForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .decorators import solo_admin, solo_usuario

def inicio(request):
    return render(request, 'inicio.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()

            Usuario.objects.create(
                user=user,
                es_admin=False
            )

            login(request, user)

            messages.success(
                request,
                "Tu cuenta fue creada con éxito."
            )
            return redirect('inicio')

        else:
            messages.error(
                request,
                "Por favor, rellena correctamente los campos."
            )
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuario/registro.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'usuario/login.html'
    authentication_form = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_admin'] = self.request.GET.get('admin') == '1'
        return context

    def get_success_url(self):
        if self.request.user.usuario.es_admin:
            return reverse_lazy('panel_admin')
        return reverse_lazy('mis_reportes')

def login_view(request):
    es_admin = request.GET.get('admin') == '1'

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if es_admin:
                if not hasattr(user, 'usuario') or not user.usuario.es_admin:
                    messages.error(request, 'No tienes permisos de administrador')
                    return redirect('login_admin')

            login(request, user)

            if user.usuario.es_admin:
                return redirect('panel_admin')
            else:
                return redirect('dashboard_usuario')
    else:
        form = LoginForm()

    return render(request, 'usuario/login.html', {
        'form': form,
        'tipo': 'admin' if es_admin else 'usuario'
    })

def get_success_url(self):
    usuario = self.request.user.usuario
    if usuario.es_admin:
        return 'panel_admin'
    else:
        return 'inicio'

@login_required    
@solo_usuario
def dashboard_usuario(request):
    return render(request, 'usuario/inicio.html')

@login_required
@solo_admin
def panel_admin(request):
    reportes = Reporte.objects.all().order_by('-fecha_reporte')
    return render(request, 'reportes/panel_admin.html', {
        'reportes': reportes
    })

@login_required
@solo_admin
def cambiar_estado(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')

        if nuevo_estado in ['Pendiente', 'En curso', 'Resuelto']:
            reporte.estado = nuevo_estado
            reporte.save()
            messages.success(
                request,
                f"El reporte fue marcado como '{nuevo_estado}'."
            )
        else:
            messages.error(request, "Estado no válido.")

    return redirect('panel_admin')

@login_required
def nuevo_reporte(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if not usuario or usuario.es_admin:
        return redirect('inicio')

    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = usuario.user
            reporte.save()
            return redirect('mis_reportes')
    else:
        form = ReporteForm()
    return render(request, 'reportes/nuevo_reporte.html', {'form': form})

def mis_reportes(request):
    # Obtenemos SIEMPRE el objeto Usuario asociado al User autenticado
    usuario = get_object_or_404(Usuario, user=request.user)

    # Si es admin, no debería estar aquí
    if usuario.es_admin:
        return redirect('panel_admin')

    # Filtramos los reportes correctamente
    reportes = Reporte.objects.filter(
        usuario=request.user,
        latitud__isnull=False,
        longitud__isnull=False
    )

    return render(
        request,
        'reportes/mis_reportes.html',
        {'reportes': reportes}
    )

@login_required
def logout_view(request):
    logout(request)
    return redirect('inicio')