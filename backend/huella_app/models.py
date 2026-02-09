# Programa: Weblla
# Veersion: 1.1
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Última Modificación: 02-02-2026
# Cambio realizado: añadido modelo para gestión de usuarios.
# Descripción:
# Modelos de datos para la aplicación de gestión de huellas de domicilios.

from django.db import models
from django.contrib.auth.models import User

class Huella(models.Model):
    """
    Modelo para gestionar líneas de huella de domicilios.
    Campos basados en el estándar de ficheros CH (COLUMNAS_CABECERAS).
    Total: 36 campos
    """
    
    # Campo 1: ID Domicilio TO (identificador único)
    iddomicilioto = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text='Identificador único del domicilio (ej: RA150541100000000000000000000000238832)'
    )
    
    # Campo 2: Código Postal
    codigopostal = models.CharField(
        max_length=5,
        db_index=True,
        help_text='Código postal (5 dígitos)'
    )
    
    # Campo 3: Provincia
    provincia = models.CharField(
        max_length=22,
        db_index=True,
        help_text='Nombre de la provincia'
    )
    
    # Campo 4: Población/Municipio
    poblacion = models.CharField(
        max_length=255,
        db_index=True,
        help_text='Nombre de la población/municipio'
    )
    
    # Campo 5: Tipo de Vía
    tipovia = models.CharField(
        max_length=17,
        help_text='Tipo de vía (CALLE, AVENIDA, PLAZA, etc.)'
    )
    
    # Campo 6: Nombre de Vía
    nombrevia = models.CharField(
        max_length=255,
        help_text='Nombre de la vía'
    )
    
    # Campo 7: ID Técnico Vía
    idtecnicovia = models.CharField(
        max_length=12,
        blank=True,
        help_text='Identificador técnico de la vía'
    )
    
    # Campo 8: Número
    numero = models.CharField(
        max_length=5,
        blank=True,
        help_text='Número de la vía'
    )
    
    # Campo 9: Bis/Duplicado
    bisduplicado = models.CharField(
        max_length=1,
        blank=True,
        help_text='Indicador de bis o duplicado'
    )
    
    # Campo 10: Bloque de la Finca
    bloquedelafinca = models.CharField(
        max_length=8,
        blank=True,
        help_text='Bloque de la finca'
    )
    
    # Campo 11: Identificador Finca/Portal
    identificadorfincaportal = models.CharField(
        max_length=3,
        blank=True,
        help_text='Identificador de finca o portal'
    )
    
    # Campo 12: Letra Finca
    letrafinca = models.CharField(
        max_length=1,
        blank=True,
        help_text='Letra de la finca'
    )
    
    # Campo 13: Escalera
    escalera = models.CharField(
        max_length=2,
        blank=True,
        help_text='Escalera del edificio'
    )
    
    # Campo 14: Planta
    planta = models.CharField(
        max_length=3,
        blank=True,
        help_text='Planta/piso'
    )
    
    # Campo 15: Mano 1 (Tipo Puerta)
    mano1 = models.CharField(
        max_length=4,
        blank=True,
        help_text='Primera mano/tipo de puerta'
    )
    
    # Campo 16: Mano 2 (Puerta Letra Número)
    mano2 = models.CharField(
        max_length=4,
        blank=True,
        help_text='Segunda mano/puerta con letra o número'
    )
    
    # Campo 17: Observaciones
    observaciones = models.TextField(
        blank=True,
        help_text='Observaciones sobre el domicilio'
    )
    
    # Campo 18: Flag Dummy
    flagdummy = models.CharField(
        max_length=1,
        blank=True,
        help_text='Flag dummy para pruebas'
    )
    
    # Campo 19: Código INE Vía
    codigoinevia = models.CharField(
        max_length=5,
        blank=True,
        help_text='Código INE de la vía'
    )
    
    # Campo 20: Código Censal
    codigocensal = models.CharField(
        max_length=10,
        blank=True,
        help_text='Código censal'
    )
    
    # Campo 21: Código PAI
    codigopai = models.CharField(
        max_length=18,
        blank=True,
        help_text='Código PAI (Padron de Asignación de Infraestructura)'
    )
    
    # Campo 22: Código OLT
    codigoolt = models.CharField(
        max_length=23,
        db_index=True,
        blank=True,
        help_text='Código OLT (Optical Line Terminal)'
    )
    
    # Campo 23: Código CTO
    codigocto = models.CharField(
        max_length=15,
        db_index=True,
        blank=True,
        help_text='Código CTO (Central Terminal Office)'
    )
    
    # Campo 24: Tipo CTO
    tipocto = models.CharField(
        max_length=55,
        blank=True,
        help_text='Tipo de CTO'
    )
    
    # Campo 25: Dirección CTO
    direccioncto = models.CharField(
        max_length=255,
        blank=True,
        help_text='Dirección de ubicación del CTO'
    )
    
    # Campo 26: Tipo Permiso
    tipopermiso = models.CharField(
        max_length=50,
        blank=True,
        help_text='Tipo de permiso o instalación'
    )
    
    # Campo 27: Tipo Caja Derivación
    tipocajaderivacion = models.CharField(
        max_length=16,
        blank=True,
        help_text='Tipo de caja de derivación'
    )
    
    # Campo 28: Número de Unidades Inmobiliarias
    numunidadesinmobiliarias = models.CharField(
        max_length=3,
        blank=True,
        help_text='Número de unidades inmobiliarias'
    )
    
    # Campo 29: Número de Viviendas
    numviviendas = models.CharField(
        max_length=3,
        blank=True,
        help_text='Número de viviendas'
    )
    
    # Campo 30: Fecha Alta (AAAAMMDD)
    fechaalta = models.CharField(
        max_length=10,
        blank=True,
        help_text='Fecha de alta en formato AAAAMMDD'
    )
    
    # Campo 31: Código Caja Derivación (Estado Operacional)
    codigocajaderivacion = models.CharField(
        max_length=50,
        blank=True,
        help_text='Código de caja de derivación / Estado operacional'
    )
    
    # Campo 32: Ubicación Caja Derivación
    ubicacioncajaderivacion = models.CharField(
        max_length=255,
        blank=True,
        help_text='Ubicación de la caja de derivación / Parcela catastral'
    )
    
    # Campo 33: COINV (Código de Inversión/Proyecto)
    coinv = models.CharField(
        max_length=10,
        blank=True,
        help_text='Código de inversión o proyecto'
    )
    
    # Campo 34: Área Comercial
    area_comercial = models.CharField(
        max_length=255,
        blank=True,
        help_text='Área comercial'
    )
    
    # Campo 35: Latitud
    lat = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        help_text='Coordenada de latitud'
    )
    
    # Campo 36: Longitud
    lng = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        help_text='Coordenada de longitud'
    )
    
    # Campos de auditoría
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Línea de Huella'
        verbose_name_plural = 'Líneas de Huella'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['iddomicilioto']),
            models.Index(fields=['codigopostal', 'provincia']),
            models.Index(fields=['codigoolt']),
            models.Index(fields=['codigocto']),
        ]
    
    def __str__(self):
        return f"{self.nombrevia} {self.numero}, {self.poblacion} ({self.iddomicilioto})"


from django.contrib.auth.models import User
from django.utils import timezone

# ==========================================
# GESTIÓN DE IMPORTACIONES DE FICHEROS
# ==========================================

class ImportacionHuella(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PROCESANDO', 'Procesando'),
        ('COMPLETADO', 'Completado'),
        ('ERROR', 'Error en validación'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='importaciones')
    fichero_original = models.FileField(upload_to='cargas/originales/')
    fichero_errores = models.FileField(upload_to='cargas/errores/', null=True, blank=True)
    fichero_normalizado = models.FileField(upload_to='cargas/normalizados/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    log_proceso = models.TextField(blank=True, help_text="Log detallado del proceso")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Importación de Huella'
        verbose_name_plural = 'Importaciones de Huella'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Importación {self.id} - {self.estado} ({self.fecha_creacion.strftime('%Y-%m-%d %H:%M')})"


# ==========================================
# NORMALIZACIÓN: TABLAS MAESTRAS (INE)
# ==========================================

class IneMunicipio(models.Model):
    """
    Corresponde al fichero YYcodmunXX.csv
    Estructura: CPRO, CMUN, DC, NOMBRE
    """
    cod_provincia = models.CharField(max_length=2, help_text="CPRO (Ej: 01)")
    cod_municipio = models.CharField(max_length=3, help_text="CMUN (Ej: 001)")
    digito_control = models.CharField(max_length=1, help_text="DC")
    nombre_oficial = models.CharField(max_length=100, help_text="NOMBRE")

    class Meta:
        indexes = [
            models.Index(fields=['cod_provincia', 'cod_municipio']),
        ]
        verbose_name = 'INE Municipio'

    def __str__(self):
        return f"{self.nombre_oficial} ({self.cod_provincia}-{self.cod_municipio})"


class InePoblacion(models.Model):
    """
    Corresponde al fichero ProvinciaXX.csv
    Estructura: Provincia, Municipio, Unidad Poblacional, Nombre...
    """
    provincia_id = models.CharField(max_length=2)
    municipio_id = models.CharField(max_length=3)
    unidad_poblacional = models.CharField(max_length=7, help_text="Código de unidad poblacional (Ej: 000000)")
    nombre = models.CharField(max_length=150)
    
    # Estos campos son extra según el CSV pero útiles para estadísticas
    total = models.IntegerField(default=0, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['provincia_id', 'municipio_id', 'unidad_poblacional']),
        ]
        verbose_name = 'INE Población'

    def __str__(self):
        return f"{self.nombre} ({self.unidad_poblacional})"


class MenuConfig(models.Model):
    """
    Configuración de menú según roles/grupos de usuarios.
    Define qué opciones del menú se muestran según el rol del usuario.
    """
    rol = models.OneToOneField(
        'auth.Group',
        on_delete=models.CASCADE,
        help_text='Grupo/Rol al que pertenece esta configuración'
    )
    
    # Opciones de menú disponibles
    mostrar_huellas = models.BooleanField(default=True, help_text='Mostrar sección de Huellas')
    mostrar_importar = models.BooleanField(default=False, help_text='Mostrar sección de Importar CSV')
    mostrar_reportes = models.BooleanField(default=False, help_text='Mostrar sección de Reportes')
    mostrar_usuarios = models.BooleanField(default=False, help_text='Mostrar gestión de usuarios')
    mostrar_resolucion = models.BooleanField(default=False, help_text='Mostrar resolución de incidencias')
    
    class Meta:
        verbose_name = 'Configuración de Menú'
        verbose_name_plural = 'Configuraciones de Menú'

    def __str__(self):
        return f"Menú - {self.rol.name}"

# Modelos para auditoría
class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('CREATED', 'Creado'),
        ('UPDATED', 'Actualizado'),
        ('DELETED', 'Eliminado'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    instance_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(null=True, blank=True, help_text="JSON con los cambios realizados")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'

    def __str__(self):
        return f'{self.action} {self.model_name} (ID: {self.instance_id}) by {self.user} at {self.timestamp}'

class UserProfile(models.Model):
    """
    Perfil extendido de usuario con campos adicionales.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    telefono = models.CharField(
        max_length=20, 
        blank=True, 
        help_text='Teléfono de contacto'
    )
    is_active_profile = models.BooleanField(
        default=True,
        help_text='Indica si el usuario está activo (soft delete)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Signal para crear perfil automáticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)