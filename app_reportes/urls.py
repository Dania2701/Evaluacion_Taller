from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nuevo_reporte/', views.nuevo_reporte, name='nuevo_reporte'),
    path('mis_reportes/', views.mis_reportes, name='mis_reportes'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('cambiar-estado/<int:reporte_id>/', views.cambiar_estado, name='cambiar_estado'),
]
