# Programa: Weblla
# Version: 1.0.1
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Última Modificación: 30-01-2026
# Descripción: Configuración local para el proyecto Django huella_project.

import os
import sys

# --- TRUCO PARA QUE NO FALLE ---
# En lugar de borrar la variable, le damos un valor "falso" temporalmente.
# Esto engaña al settings.py original para que no falle al intentar leerla.

#os.environ['DATABASE_URL'] = 'sqlite:///dummy.db'
os.environ['DATABASE_URL'] = 'postgres://app:app@localhost:5432/appdb'

# Configuración de Celery para desarrollo local
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Ahora importamos la configuración original (se tragará la URL falsa sin error)
from .settings import *

# --- CONFIGURACIÓN REAL ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'appdb',
        'USER': 'app',
        'PASSWORD': 'app',
        'HOST': 'localhost', 
        'PORT': '5432',
    }
}

# Configuración de desarrollo
DEBUG = True
ALLOWED_HOSTS = ['*']

# CORS permisivo para desarrollo local
CORS_ALLOW_ALL_ORIGINS = True

# Deshabilitar HTTPS en desarrollo
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False