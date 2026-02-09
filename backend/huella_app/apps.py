# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción: Configuración de la aplicación HuellaApp en Django.

from django.apps import AppConfig


class HuellaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'huella_app'
    verbose_name = 'Gestión de Huellas'

    def ready(self):
        import huella_app.signals  # noqa
