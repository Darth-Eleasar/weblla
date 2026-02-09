# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 30-01-2026
# Descripción:
# Configuración de Celery para el proyecto Django "huella_project"

import os
from celery import Celery

# Configurar el módulo de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huella_project.settings')

app = Celery('huella_project')

# Leer configuración desde settings.py con prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir tareas automáticamente en todas las apps instaladas
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
