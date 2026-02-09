# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción:
# Comando de gestión de Django para importar datos maestros del INE desde ficheros CSV.
# Uso: python manage.py importar_ine <ruta_municipios.csv> <ruta_poblacion.csv>


"""
Comando para importar datos maestros del INE.

Uso: python manage.py importar_ine <ruta_municipios.csv> <ruta_poblacion.csv>

Ejemplo:
python manage.py importar_ine ../datos/15codmun.csv ../datos/Provincia15.csv
"""

import csv
from django.core.management.base import BaseCommand
from huella_app.models import IneMunicipio, InePoblacion


class Command(BaseCommand):
    help = 'Importa los datos maestros del INE (municipios y poblaciones)'

    def add_arguments(self, parser):
        parser.add_argument(
            'fichero_municipios',
            type=str,
            help='Ruta al fichero de municipios (YYcodmunXX.csv)'
        )
        parser.add_argument(
            'fichero_poblacion',
            type=str,
            help='Ruta al fichero de poblaciones (ProvinciaXX.csv)'
        )
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpiar datos existentes antes de importar'
        )

    def handle(self, *args, **options):
        fichero_municipios = options['fichero_municipios']
        fichero_poblacion = options['fichero_poblacion']
        limpiar = options.get('limpiar', False)

        # Limpiar datos si se especifica
        if limpiar:
            IneMunicipio.objects.all().delete()
            InePoblacion.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Datos existentes eliminados'))

        # 1. Importar municipios
        self.stdout.write(f'\n📍 Importando municipios desde {fichero_municipios}...')
        try:
            municipios_creados = 0
            with open(fichero_municipios, 'r', encoding='utf-8') as f:
                # Saltar las 2 primeras líneas
                f.readline()
                f.readline()
                
                reader = csv.DictReader(f, fieldnames=['cod_provincia', 'cod_municipio', 'digito_control', 'nombre_oficial'])
                
                for row in reader:
                    if not row['cod_provincia'] or row['cod_provincia'].startswith('CPRO'):
                        continue
                    
                    municipio, created = IneMunicipio.objects.get_or_create(
                        cod_provincia=row['cod_provincia'].strip(),
                        cod_municipio=row['cod_municipio'].strip(),
                        defaults={
                            'digito_control': row['digito_control'].strip(),
                            'nombre_oficial': row['nombre_oficial'].strip(),
                        }
                    )
                    if created:
                        municipios_creados += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ {municipios_creados} municipios importados')
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'  ❌ No se encontró el fichero: {fichero_municipios}')
            )
            return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ❌ Error importando municipios: {e}')
            )
            return

        # 2. Importar poblaciones
        self.stdout.write(f'\n🏘️ Importando poblaciones desde {fichero_poblacion}...')
        try:
            poblaciones_creadas = 0
            with open(fichero_poblacion, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    if not row or 'Provincia' not in row:
                        continue
                    
                    try:
                        poblacion, created = InePoblacion.objects.get_or_create(
                            provincia_id=row['Provincia'].strip(),
                            municipio_id=row['Municipio'].strip(),
                            unidad_poblacional=row['Unidad Poblacional'].strip(),
                            defaults={
                                'nombre': row['Unidad Poblacional'].strip(),
                                'total': int(row.get('Total 2023', 0) or 0),
                            }
                        )
                        if created:
                            poblaciones_creadas += 1
                    except (KeyError, ValueError) as e:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ Fila con datos inválidos (ignorada): {e}')
                        )
                        continue
            
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ {poblaciones_creadas} poblaciones importadas')
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'  ❌ No se encontró el fichero: {fichero_poblacion}')
            )
            return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ❌ Error importando poblaciones: {e}')
            )
            return

        self.stdout.write(
            self.style.SUCCESS('\n✓ Datos del INE importados exitosamente')
        )
