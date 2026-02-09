# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Descripción:
# Señales para auditar cambios en los modelos Huella, ImportacionHuella, IneMunicipio, InePoblacion y MenuConfig.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Huella, ImportacionHuella, IneMunicipio, InePoblacion, MenuConfig, AuditLog

def get_current_user():
    # Esto es un marcador de posición. En una aplicación real, obtendrías el usuario de la solicitud.
    # Para las señales, esto puede ser complicado. Un patrón común es almacenar el usuario en una variable local del hilo.
    # Por ahora, devolveremos None o un usuario predeterminado si está disponible.
    return None # O User.objects.get(username='system') if you have a system user

@receiver(post_save, sender=Huella)
@receiver(post_save, sender=ImportacionHuella)
@receiver(post_save, sender=IneMunicipio)
@receiver(post_save, sender=InePoblacion)
@receiver(post_save, sender=MenuConfig)
def log_model_save(sender, instance, created, **kwargs):
    action = 'CREATED' if created else 'UPDATED'
    user = get_current_user() # Marcador de posición para obtener el usuario actual

    changes = {}
    if not created:
        # Para las actualizaciones, necesitaríamos comparar los datos antiguos con los nuevos.
        # Este es un enfoque simplificado. Una solución más robusta implicaría obtener la instancia antigua.
        pass # Por ahora, solo registraremos la acción sin cambios detallados para las actualizaciones

    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=sender.__name__,
        instance_id=instance.pk,
        changes=changes
    )

@receiver(post_delete, sender=Huella)
@receiver(post_delete, sender=ImportacionHuella)
@receiver(post_delete, sender=IneMunicipio)
@receiver(post_delete, sender=InePoblacion)
@receiver(post_delete, sender=MenuConfig)
def log_model_delete(sender, instance, **kwargs):
    user = get_current_user() # Marcador de posición para obtener el usuario actual

    AuditLog.objects.create(
        user=user,
        action='DELETED',
        model_name=sender.__name__,
        instance_id=instance.pk,
        changes={} # No se necesitan cambios para la eliminación
    )