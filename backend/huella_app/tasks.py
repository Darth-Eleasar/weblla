# Programa: Weblla
# Veersion: 1.0
# Autor: Equipo Weblla
# Fecha: 30-01-2026
# Última Modificación:
# Descripción: Ejemplos de tareas asíncronas con Celery
# Tareas asíncronas para la aplicación Huella
# Uso del código:
# En cualquier vista o servicio
#   from huella_app.tasks import procesar_archivo, enviar_email

    # Ejecutar tarea asíncrona
#   procesar_archivo.delay(archivo_id=123)

    # Con opciones adicionales
    # enviar_email.apply_async(
    #     args=['user@example.com', 'Asunto', 'Mensaje'],
    #     countdown=60  # ejecutar en 60 segundos
    # )

    # Obtener resultado
    # resultado = procesar_archivo.delay(123)
    # print(resultado.id)  # ID de la tarea
    # print(resultado.status)  # Estado: PENDING, STARTED, SUCCESS, FAILURE
    # print(resultado.get(timeout=30))  # Esperar resultado (bloquea)

from celery import shared_task
import time


@shared_task
def procesar_archivo(archivo_id):
    """Procesa un archivo en segundo plano"""
    # Simular procesamiento largo
    time.sleep(10)
    print(f"Archivo {archivo_id} procesado")
    return f"Archivo {archivo_id} completado"


@shared_task
def enviar_email(destinatario, asunto, mensaje):
    """Envía un email en segundo plano"""
    # lógica de envío de email
    print(f"Email enviado a {destinatario}")
    return True


@shared_task
def limpiar_logs():
    """Tarea programada para limpiar logs antiguos"""
    print("Limpiando logs...")
    return "Logs limpiados"
