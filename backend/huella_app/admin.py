# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción: Configuración del panel de administración para la aplicación Huella.

from django.contrib import admin
from .models import Huella, MenuConfig, ImportacionHuella, IneMunicipio, InePoblacion, AuditLog

# Registro del modelo Huella en el admin de Django
@admin.register(Huella)
class HuellaAdmin(admin.ModelAdmin):
    """Admin para gestionar líneas de huella."""
    
    list_display = [
        'iddomicilioto',
        'nombrevia',
        'numero',
        'poblacion',
        'codigopostal',
        'provincia',
        'codigoolt',
        'codigocto',
        'created',
    ]
    
    list_filter = [
        'provincia',
        'codigopostal',
        'poblacion',
        'tipovia',
        'created',
    ]
    
    search_fields = [
        'iddomicilioto',
        'nombrevia',
        'provincia',
        'poblacion',
        'codigopostal',
        'codigoolt',
        'codigocto',
    ]
    
    readonly_fields = ['created', 'updated']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('iddomicilioto',)
        }),
        ('Ubicación', {
            'fields': (
                'codigopostal',
                'provincia',
                'poblacion',
                'tipovia',
                'nombrevia',
                'numero',
                'bisduplicado',
            )
        }),
        ('Finca', {
            'fields': (
                'bloquedelafinca',
                'identificadorfincaportal',
                'letrafinca',
                'escalera',
                'planta',
            ),
            'classes': ('collapse',)
        }),
        ('Puertas', {
            'fields': ('mano1', 'mano2'),
            'classes': ('collapse',)
        }),
        ('Infraestructura', {
            'fields': (
                'codigoolt',
                'codigocto',
                'tipocto',
                'direccioncto',
                'tipocajaderivacion',
                'codigocajaderivacion',
                'ubicacioncajaderivacion',
            ),
            'classes': ('collapse',)
        }),
        ('Datos Técnicos', {
            'fields': (
                'idtecnicovia',
                'codigoinevia',
                'codigocensal',
                'codigopai',
                'tipopermiso',
                'coinv',
                'area_comercial',
            ),
            'classes': ('collapse',)
        }),
        ('Inmobiliario', {
            'fields': (
                'numunidadesinmobiliarias',
                'numviviendas',
            ),
            'classes': ('collapse',)
        }),
        ('Datos Adicionales', {
            'fields': (
                'fechaalta',
                'flagdummy',
                'lat',
                'lng',
                'observaciones',
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created']

# Registro del modelo MenuConfig en el admin de Django
@admin.register(MenuConfig)
class MenuConfigAdmin(admin.ModelAdmin):
    """Admin para gestionar la configuración de menú según roles."""
    
    list_display = ['rol']
    list_filter = ['rol']

# Registro del modelo ImportacionHuella en el admin de Django
@admin.register(ImportacionHuella)
class ImportacionHuellaAdmin(admin.ModelAdmin):
    """Admin para gestionar importaciones de CSV."""
    
    list_display = [
        'id',
        'usuario_nombre',
        'fichero_original',
        'estado',
        'fecha_creacion',
    ]
    
    list_filter = ['estado', 'fecha_creacion']
    
    search_fields = ['usuario__username']
    
    readonly_fields = ['usuario', 'estado', 'log_proceso', 'fichero_errores', 'fichero_normalizado', 'fecha_creacion']
    
    def usuario_nombre(self, obj):
        return obj.usuario.username if obj.usuario else 'Sistema'
    usuario_nombre.short_description = 'Usuario'

# Registro del modelo IneMunicipio en el admin de Django
@admin.register(IneMunicipio)
class IneMunicipioAdmin(admin.ModelAdmin):
    """Admin para gestionar municipios del INE."""
    
    list_display = [
        'cod_provincia',
        'cod_municipio',
        'nombre_oficial',
    ]
    
    list_filter = ['cod_provincia']
    
    search_fields = ['nombre_oficial', 'cod_provincia', 'cod_municipio']

# Registro del modelo InePoblacion en el admin de Django
@admin.register(InePoblacion)
class InePoblacionAdmin(admin.ModelAdmin):
    """Admin para gestionar poblaciones del INE."""
    
    list_display = [
        'provincia_id',
        'municipio_id',
        'nombre',
        'unidad_poblacional',
    ]
    
    list_filter = ['provincia_id', 'municipio_id']
    
    search_fields = ['nombre', 'provincia_id', 'municipio_id']

# Registro del modelo AuditLog en el admin de Django
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'instance_id')
    list_filter = ('action', 'model_name', 'user')
    search_fields = ('user__username', 'model_name', 'instance_id')
    readonly_fields = ('timestamp', 'user', 'action', 'model_name', 'instance_id', 'changes')
    date_hierarchy = 'timestamp'