from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Reporte, Usuario


# Registro de nuevos usuarios
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    telefono = forms.CharField(required=False, label="Teléfono (opcional)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Se crea también la instancia en la tabla Usuario
            Usuario.objects.create(
                user=user,
                telefono=self.cleaned_data.get('telefono', '')
            )
        return user


# Login de usuarios
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# Formulario para crear reportes
class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['descripcion', 'ubicacion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }
