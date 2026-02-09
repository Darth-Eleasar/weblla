# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción: Configuración de URLs para el proyecto Django huella_project.

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('huella_app.urls')),
]
