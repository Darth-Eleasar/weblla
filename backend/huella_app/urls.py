# Programa: Weblla
# Veersion: 1.1
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Última Modificación: 02-02-2026
# Cambios realizados: Actualización de rutas para gestión de usuarios.
# Descripción:
# Archivo de rutas para la aplicación huella_app.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HuellaViewSet, ImportacionViewSet, LoginView, LogoutView, 
    UserDetailView, MenuView, UserViewSet
)

router = DefaultRouter()
router.register(r'huellas', HuellaViewSet, basename='huella')
router.register(r'importaciones', ImportacionViewSet, basename='importacion')
router.register(r'usuarios', UserViewSet, basename='usuario')

app_name = 'huella_app'

urlpatterns = [
    path('', include(router.urls)),
    # Endpoints de autenticación
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', UserDetailView.as_view(), name='user-detail'),
    path('auth/menu/', MenuView.as_view(), name='menu'),
]