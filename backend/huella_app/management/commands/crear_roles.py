# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción:
# Comando de gestión de Django para crear roles (grupos) y asignar permisos y configuraciones de menú.

"""
Comando para crear los roles (grupos) del sistema.

Uso: python manage.py crear_roles
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from huella_app.models import Huella, ImportacionHuella, IneMunicipio, InePoblacion, MenuConfig


class Command(BaseCommand):
    help = 'Crea los grupos de usuarios (Admin, Ingeniería, Técnico)'

    def handle(self, *args, **options):
        roles = {
            'Admin': {
                'permisos': [
                    'add_huella', 'change_huella', 'delete_huella', 'view_huella',
                    'add_importacionhuella', 'change_importacionhuella', 'delete_importacionhuella', 'view_importacionhuella',
                    'add_inemunicipio', 'change_inemunicipio', 'delete_inemunicipio', 'view_inemunicipio',
                    'add_inepoblacion', 'change_inepoblacion', 'delete_inepoblacion', 'view_inepoblacion',
                    'add_user', 'change_user', 'delete_user', 'view_user',
                ],
                'menu': {
                    'mostrar_huellas': True,
                    'mostrar_importar': True,
                    'mostrar_reportes': True,
                    'mostrar_usuarios': True,
                    'mostrar_resolucion': True,
                }
            },
            'Ingeniería': {
                'permisos': [
                    'view_huella', 'change_huella',
                    'view_importacionhuella', 'change_importacionhuella',
                    'view_inemunicipio',
                    'view_inepoblacion',
                    'view_user',
                ],
                'menu': {
                    'mostrar_huellas': True,
                    'mostrar_importar': True,
                    'mostrar_reportes': True,
                    'mostrar_usuarios': False,
                    'mostrar_resolucion': True,
                }
            },
            'Técnico': {
                'permisos': [
                    'view_huella',
                    'view_importacionhuella',
                    'view_inemunicipio',
                    'view_inepoblacion',
                ],
                'menu': {
                    'mostrar_huellas': True,
                    'mostrar_importar': False,
                    'mostrar_reportes': False,
                    'mostrar_usuarios': False,
                    'mostrar_resolucion': False,
                }
            },
        }

        for rol_nombre, config in roles.items():
            group, created = Group.objects.get_or_create(name=rol_nombre)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Grupo "{rol_nombre}" creado')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Grupo "{rol_nombre}" ya existía')
                )
            
            # Agregar permisos al grupo
            permisos = []
            for permiso_codename in config['permisos']:
                try:
                    # Buscar el permiso en los modelos
                    for modelo in [Huella, ImportacionHuella, IneMunicipio, InePoblacion]:
                        perm = Permission.objects.filter(
                            codename=permiso_codename,
                            content_type=ContentType.objects.get_for_model(modelo)
                        ).first()
                        if perm:
                            permisos.append(perm)
                            break
                    
                    # Si no encontró en nuestros modelos, buscar en auth (usuarios)
                    if not permisos or permisos[-1].codename != permiso_codename:
                        from django.contrib.auth.models import User
                        perm = Permission.objects.filter(
                            codename=permiso_codename,
                            content_type=ContentType.objects.get_for_model(User)
                        ).first()
                        if perm:
                            permisos.append(perm)
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ No se pudo asignar permiso "{permiso_codename}": {e}')
                    )
            
            group.permissions.set(permisos)
            self.stdout.write(
                self.style.SUCCESS(f'  → {len(permisos)} permisos asignados a "{rol_nombre}"')
            )
            
            # Crear o actualizar configuración de menú
            menu_config, menu_created = MenuConfig.objects.update_or_create(
                rol=group,
                defaults={
                    'mostrar_huellas': config['menu']['mostrar_huellas'],
                    'mostrar_importar': config['menu']['mostrar_importar'],
                    'mostrar_reportes': config['menu']['mostrar_reportes'],
                    'mostrar_usuarios': config['menu']['mostrar_usuarios'],
                    'mostrar_resolucion': config['menu']['mostrar_resolucion'],
                }
            )
            if menu_created:
                self.stdout.write(
                    self.style.SUCCESS(f'  → Configuración de menú creada para "{rol_nombre}"')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Sistema de roles creado exitosamente')
        )

