# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción:
# Este archivo es el punto de entrada para las tareas administrativas de Django.
# Detecta automáticamente si existe un archivo de configuración local (settings_local.py)
# y lo utiliza en lugar del archivo de configuración predeterminado (settings.py).

"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Detectar automáticamente si existe settings_local
    settings_module = 'huella_project.settings'
    
    try:
        import huella_project.settings_local
        settings_module = 'huella_project.settings_local'
        print("✓ Usando configuración local (settings_local.py)")
    except ImportError:
        print("✓ Usando configuración de producción (settings.py)")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django, ¿Estás seguro de que está instalado y"
            " disponible en la variable PYTHONPATH?"
            " ¿Está activado el entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()