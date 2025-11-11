from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Reporte, Usuario
from .forms import ReporteForm, RegistroForm, LoginForm
from django.contrib import messages

def inicio(request):
    return render(request, 'inicio.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear el objeto Usuario asociado al nuevo User
            Usuario.objects.create(user=user, es_admin=False)
            messages.success(request, "Tu cuenta fue creada con éxito. Ahora puedes iniciar sesión.")
            return redirect('login')  # Redirige correctamente al login
        else:
            messages.error(request, "Por favor, rellena correctamente los campos del formulario.")
    else:
        form = RegistroForm()

    return render(request, 'usuario/registro.html', {'form': form})


def login_view(request):
    es_admin_login = request.GET.get('admin') == '1'
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                usuario = Usuario.objects.get(user=user)
                if usuario.es_admin:
                    return redirect('panel_admin')
                else:
                    return redirect('mis_reportes')
            except Usuario.DoesNotExist:
                messages.error(request, "Tu cuenta no está correctamente vinculada.")
                logout(request)
                return redirect('login')
    else:
        form = LoginForm()

    contexto = {
        'form': form,
        'es_admin_login': es_admin_login
    }
    return render(request, 'usuario/login.html', contexto)
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def panel_admin(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        if not usuario.es_admin:
            messages.error(request, "No tienes permisos para acceder a esta página.")
            return redirect('inicio')
    except Usuario.DoesNotExist:
        messages.error(request, "Tu cuenta no está correctamente configurada.")
        return redirect('inicio')

    # Si es admin, muestra todos los reportes
    reportes = Reporte.objects.all().order_by('-fecha_reporte')
    return render(request, 'panel_admin.html', {'reportes': reportes})

@login_required
def cambiar_estado(request, reporte_id):
    try:
        usuario = Usuario.objects.get(user=request.user)
        if not usuario.es_admin:
            messages.error(request, "No tienes permisos para modificar reportes.")
            return redirect('inicio')
    except Usuario.DoesNotExist:
        messages.error(request, "Tu cuenta no está correctamente configurada.")
        return redirect('inicio')

    reporte = get_object_or_404(Reporte, id=reporte_id)
    nuevo_estado = request.GET.get('estado')

    if nuevo_estado in ['Pendiente', 'En curso', 'Resuelto']:
        reporte.estado = nuevo_estado
        reporte.save()
        messages.success(request, f"El reporte fue marcado como '{nuevo_estado}'.")
    else:
        messages.error(request, "Estado no válido.")

    return redirect('panel_admin')

@login_required
def nuevo_reporte(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if not usuario or usuario.es_admin:
        return redirect('inicio')

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = usuario
            reporte.save()
            return redirect('mis_reportes')
    else:
        form = ReporteForm()
    return render(request, 'reportes/nuevo_reporte.html', {'form': form})


@login_required
def mis_reportes(request):
    usuario = Usuario.objects.filter(user=request.user).first()
    if not usuario or usuario.es_admin:
        return redirect('panel_admin')
    reportes = Reporte.objects.filter(usuario=usuario)
    return render(request, 'reportes/mis_reportes.html', {'reportes': reportes})


@login_required
@user_passes_test(lambda u: Usuario.objects.filter(user=u, es_admin=True).exists())
def panel_admin(request):
    reportes = Reporte.objec
