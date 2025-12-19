from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Reporte
from django.contrib.auth.decorators import login_required

# Registro de nuevos usuarios
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-300'
        })
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-300'
        })
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-300'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-blue-300'
            }),
        }

# Formulario de inicio de sesión
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )

# Formulario para crear un nuevo reporte
class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = [
            'titulo',
            'descripcion',
            'referencia',
            'latitud',
            'longitud',
            'foto'
        ]

        widgets = {
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        latitud = cleaned_data.get('latitud')
        longitud = cleaned_data.get('longitud')

        if not latitud or not longitud:
            raise forms.ValidationError("Debes seleccionar una ubicación en el mapa.")
        return cleaned_data

@login_required
def nuevo_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, 'Reporte creado exitosamente.')
            return redirect('mis_reportes')
    else:
        form = ReporteForm()
    return render(request, 'reportes/nuevo_reporte.html', {'form': form})