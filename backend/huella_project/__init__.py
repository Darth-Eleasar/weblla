# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 30-01-2026
# Descripción: Inicialización del paquete huella_project y configuración de Celery.

from .celery import app as celery_app

__all__ = ('celery_app',)