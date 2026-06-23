from django.urls import path
from . import views

urlpatterns = [
    # Login
    path('', views.login_view, name='login'),
    path('inicio/', views.inicio, name='inicio'),
    path('logout/', views.logout_view, name='logout'),

    # Propiedades
    path('listarPropiedades/', views.listarPropiedades, name='listarPropiedades'),
    path('nuevaPropiedad/', views.nuevaPropiedad, name='nuevaPropiedad'),
    path('guardarPropiedad/', views.guardarPropiedad, name='guardarPropiedad'),
    path('editarPropiedad/<int:id>/', views.editarPropiedad, name='editarPropiedad'),
    path('actualizarPropiedad/', views.actualizarPropiedad, name='actualizarPropiedad'),
    path('eliminarPropiedad/<int:id>/', views.eliminarPropiedad, name='eliminarPropiedad'),

    # Contratos
    path('listarContratos/', views.listarContratos, name='listarContratos'),
    path('nuevoContrato/', views.nuevoContrato, name='nuevoContrato'),
    path('guardarContrato/', views.guardarContrato, name='guardarContrato'),
    path('editarContrato/<int:id>/', views.editarContrato, name='editarContrato'),
    path('actualizarContrato/', views.actualizarContrato, name='actualizarContrato'),
    path('eliminarContrato/<int:id>/', views.eliminarContrato, name='eliminarContrato'),
]