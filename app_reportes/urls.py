from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Usuario
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('nuevo_reporte/', views.nuevo_reporte, name='nuevo_reporte'),
    path('mis_reportes/', views.mis_reportes, name='mis_reportes'),

    # Admin
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('cambiar-estado/<int:reporte_id>/',views.cambiar_estado,name='cambiar_estado'),
]