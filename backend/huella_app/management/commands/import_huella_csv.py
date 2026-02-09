# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción:
# Comando de gestión de Django para importar líneas de huella desde un archivo CSV.
# El CSV debe tener el separador ; y 36 columnas en el orden definido por COLUMNAS_CABECERAS.
# El comando maneja errores, permite opciones de verbosidad y puede omitir filas con errores si se especifica.

import csv
from django.core.management.base import BaseCommand, CommandError
from huella_app.models import Huella


class Command(BaseCommand):
    help = 'Importa líneas de huella desde un archivo CSV. Espera separador ; y 36 columnas en orden COLUMNAS_CABECERAS'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            type=str,
            help='Ruta al archivo CSV a importar (ej: /ruta/archivo.csv)'
        )
        parser.add_argument(
            '--delimiter',
            type=str,
            default=';',
            help='Delimitador del CSV (default: ;)'
        )
        parser.add_argument(
            '--skip-errors',
            action='store_true',
            help='Continúa importación aunque haya errores en filas'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Muestra información detallada de cada fila'
        )

    def handle(self, *args, **options):
        import os
        
        path = options['csv_path']
        delimiter = options['delimiter']
        skip_errors = options['skip_errors']
        verbose = options['verbose']
        
        # Verificar que el archivo existe
        if not os.path.exists(path):
            # Intentar ruta relativa
            path_alt = os.path.join(os.getcwd(), path)
            if not os.path.exists(path_alt):
                raise CommandError(f'Archivo no encontrado: {path}\nTambién probé: {path_alt}')
            path = path_alt
        
        self.stdout.write(self.style.SUCCESS(f'✓ Archivo encontrado: {path}'))
        self.stdout.write(f'  Delimitador: "{delimiter}"\n')
        
        # Orden esperado de columnas del estándar CH
        # NOTA: El CSV real tiene solo 27 campos, no 36
        # Mapeo: pos CSV → campo modelo
        COLUMNAS_CABECERAS = [
            'iddomicilioto',                    # 1
            'codigopostal',                     # 2
            'provincia',                        # 3
            'poblacion',                        # 4
            'tipovia',                          # 5
            'nombrevia',                        # 6
            'idtecnicovia',                     # 7
            'numero',                           # 8
            'bisduplicado',                     # 9
            'bloquedelafinca',                  # 10
            'identificadorfincaportal',         # 11
            'letrafinca',                       # 12
            'escalera',                         # 13
            'planta',                           # 14
            'mano1',                            # 15
            'mano2',                            # 16
            'observaciones',                    # 17
            'flagdummy',                        # 18
            'codigoinevia',                     # 19
            'codigocensal',                     # 20
            'codigopai',                        # 21
            'codigoolt',                        # 22
            'codigocto',                        # 23
            'tipocto',                          # 24
            'direccioncto',                     # 25
            'tipopermiso',                      # 26
            'tipocajaderivacion',               # 27
            'numviviendas',
            'fechaalta',
            'codigocajaderivacion',
            'ubicacioncajaderivacion',
            'coinv',
            'area_comercial',
            'lat',
            'lng'
        ]
        
        created = 0
        updated = 0
        errors = 0
        
        try:
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=delimiter)
                
                # Leer primera fila para mostrar info
                primera_fila_original = None
                
                for num_fila, row in enumerate(reader, 1):
                    if num_fila == 1:
                        primera_fila_original = row
                        self.stdout.write(f'Primera fila: {len(row)} columnas')
                        if verbose:
                            self.stdout.write(f'  Contenido: {row[:3]}...\n')
                    
                    try:
                        # Validar que tenga al menos 27 columnas (CSV real tiene 27, modelo tiene 36)
                        # Las columnas faltantes se completarán con valores vacíos
                        NUM_CAMPOS_ESPERADOS = 27  # CSV real tiene 27 campos
                        
                        if len(row) < NUM_CAMPOS_ESPERADOS:
                            error_msg = f'Fila {num_fila}: esperadas al menos {NUM_CAMPOS_ESPERADOS} columnas, se encontraron {len(row)}'
                            if verbose:
                                error_msg += f'\nContenido: {row}'
                            if skip_errors:
                                self.stdout.write(self.style.WARNING(error_msg))
                                errors += 1
                                continue
                            else:
                                raise CommandError(error_msg)
                        
                        # Truncar a 27 campos si hay más (por compatibilidad)
                        row = row[:NUM_CAMPOS_ESPERADOS]
                        
                        # Crear diccionario de datos
                        datos = dict(zip(COLUMNAS_CABECERAS, row))
                        
                        # Campo obligatorio: iddomicilioto
                        if not datos.get('iddomicilioto', '').strip():
                            error_msg = f'Fila {num_fila}: iddomicilioto está vacío'
                            if skip_errors:
                                self.stdout.write(self.style.WARNING(error_msg))
                                errors += 1
                                continue
                            else:
                                raise CommandError(error_msg)
                        
                        # Campos obligatorios: codigopostal, provincia, poblacion
                        campos_obligatorios = ['codigopostal', 'provincia', 'poblacion']
                        for campo in campos_obligatorios:
                            if not datos.get(campo, '').strip():
                                error_msg = f'Fila {num_fila}: {campo} está vacío'
                                if skip_errors:
                                    self.stdout.write(self.style.WARNING(error_msg))
                                    errors += 1
                                    continue
                                else:
                                    raise CommandError(error_msg)
                        
                        # Convertir lat/lng a decimal si existen
                        try:
                            lat = float(datos.get('lat', '').strip()) if datos.get('lat', '').strip() else None
                        except ValueError:
                            lat = None
                        
                        try:
                            lng = float(datos.get('lng', '').strip()) if datos.get('lng', '').strip() else None
                        except ValueError:
                            lng = None
                        
                        # Obtener o crear huella
                        huella, es_nueva = Huella.objects.get_or_create(
                            iddomicilioto=datos['iddomicilioto'],
                            defaults={
                                'codigopostal': datos['codigopostal'],
                                'provincia': datos['provincia'],
                                'poblacion': datos['poblacion'],
                                'tipovia': datos['tipovia'],
                                'nombrevia': datos['nombrevia'],
                                'idtecnicovia': datos.get('idtecnicovia', ''),
                                'numero': datos.get('numero', ''),
                                'bisduplicado': datos.get('bisduplicado', ''),
                                'bloquedelafinca': datos.get('bloquedelafinca', ''),
                                'identificadorfincaportal': datos.get('identificadorfincaportal', ''),
                                'letrafinca': datos.get('letrafinca', ''),
                                'escalera': datos.get('escalera', ''),
                                'planta': datos.get('planta', ''),
                                'mano1': datos.get('mano1', ''),
                                'mano2': datos.get('mano2', ''),
                                'observaciones': datos.get('observaciones', ''),
                                'flagdummy': datos.get('flagdummy', ''),
                                'codigoinevia': datos.get('codigoinevia', ''),
                                'codigocensal': datos.get('codigocensal', ''),
                                'codigopai': datos.get('codigopai', ''),
                                'codigoolt': datos.get('codigoolt', ''),
                                'codigocto': datos.get('codigocto', ''),
                                'tipocto': datos.get('tipocto', ''),
                                'direccioncto': datos.get('direccioncto', ''),
                                'tipopermiso': datos.get('tipopermiso', ''),
                                'tipocajaderivacion': datos.get('tipocajaderivacion', ''),
                                'numunidadesinmobiliarias': datos.get('numunidadesinmobiliarias', ''),
                                'numviviendas': datos.get('numviviendas', ''),
                                'fechaalta': datos.get('fechaalta', ''),
                                'codigocajaderivacion': datos.get('codigocajaderivacion', ''),
                                'ubicacioncajaderivacion': datos.get('ubicacioncajaderivacion', ''),
                                'coinv': datos.get('coinv', ''),
                                'area_comercial': datos.get('area_comercial', ''),
                                'lat': lat,
                                'lng': lng,
                            }
                        )
                        
                        if es_nueva:
                            created += 1
                            if verbose:
                                self.stdout.write(self.style.SUCCESS(f'✓ Creada fila {num_fila}: {huella.iddomicilioto}'))
                        else:
                            updated += 1
                            if verbose:
                                self.stdout.write(self.style.WARNING(f'⊗ Actualizada fila {num_fila}: {huella.iddomicilioto}'))
                    
                    except Exception as e:
                        error_msg = f'Fila {num_fila}: Error al procesar: {str(e)}'
                        if verbose:
                            import traceback
                            error_msg += f'\nTraceback: {traceback.format_exc()}'
                        if skip_errors:
                            self.stdout.write(self.style.ERROR(error_msg))
                            errors += 1
                        else:
                            raise CommandError(error_msg)
        
        except FileNotFoundError:
            raise CommandError(f'Archivo no encontrado: {path}')
        except Exception as e:
            raise CommandError(f'Error al leer archivo: {str(e)}')
        
        # Resumen final
        self.stdout.write(self.style.SUCCESS(f'\n╔════════════════════════════════════════════╗'))
        self.stdout.write(self.style.SUCCESS(f'║ Importación completada                    ║'))
        self.stdout.write(self.style.SUCCESS(f'╠════════════════════════════════════════════╣'))
        self.stdout.write(self.style.SUCCESS(f'║ ✓ Creadas:      {created:>24} ║'))
        self.stdout.write(self.style.SUCCESS(f'║ ⊗ Actualizadas: {updated:>24} ║'))
        self.stdout.write(self.style.SUCCESS(f'║ ✗ Errores:      {errors:>24} ║'))
        self.stdout.write(self.style.SUCCESS(f'║ Total:          {created + updated:>24} ║'))
        self.stdout.write(self.style.SUCCESS(f'╚════════════════════════════════════════════╝'))
