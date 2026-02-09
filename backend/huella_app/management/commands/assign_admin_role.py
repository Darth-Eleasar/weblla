# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción:
# Comando de gestión para asignar el rol Admin a un usuario específico.

"""Comando para asignar el rol Admin al usuario admin"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Asigna el rol Admin al usuario admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Nombre de usuario (default: admin)'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(f"Usuario '{username}' no encontrado")
            )
            return

        try:
            admin_group = Group.objects.get(name='Admin')
        except Group.DoesNotExist:
            self.stderr.write(
                self.style.ERROR("Grupo 'Admin' no encontrado")
            )
            return

        user.groups.add(admin_group)
        
        self.stdout.write(
            self.style.SUCCESS(f"Usuario '{username}' agregado al grupo 'Admin'")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Grupos del usuario: {', '.join(user.groups.values_list('name', flat=True))}"
            )
        )