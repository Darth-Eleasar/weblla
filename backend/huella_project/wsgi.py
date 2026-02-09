# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción: Configuración WSGI para el proyecto Django huella_project.

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huella_project.settings')
application = get_wsgi_application()
