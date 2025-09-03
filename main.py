# main.py
# Cloud Function en Python que se activa al subir archivos a un bucket de Cloud Storage.
# Extrae metadatos del archivo y registra eventos en Cloud Logging.

import functions_framework
import logging

# Se define la función que se ejecuta al ocurrir un evento en Cloud Storage.
# @functions_framework.cloud_event indica que la función recibe un CloudEvent.
@functions_framework.cloud_event
def metadata(cloud_event):
    """
    Función que procesa eventos de Cloud Storage.

    Parámetros:
    cloud_event (CloudEvent): Evento disparado por Cloud Storage
    """
    try:
        # Extraemos los datos del evento
        data = cloud_event.data

        # Información general del evento
        event_id = cloud_event["id"]           # ID único del evento
        event_type = cloud_event["type"]       # Tipo de evento (ej. google.cloud.storage.object.v1.finalized)

        # Metadatos del archivo
        bucket = data.get("bucket")            # Nombre del bucket donde se subió el archivo
        name = data.get("name")                # Nombre del archivo
        metageneration = data.get("metageneration")  # Versión del archivo
        size = data.get("size")                # Tamaño del archivo en bytes
        content_type = data.get("contentType") # Tipo MIME del archivo
        time_created = data.get("timeCreated") # Fecha de creación del archivo
        updated = data.get("updated")          # Fecha de última actualización

        # Logging de la información obtenida
        # Se utiliza logging.info para que aparezca en Cloud Logging
        logging.info(f"Event ID: {event_id}")
        logging.info(f"Event type: {event_type}")
        logging.info(f"Bucket: {bucket}")
        logging.info(f"File: {name}")
        logging.info(f"Metageneration: {metageneration}")
        logging.info(f"Size: {size} bytes")
        logging.info(f"Content type: {content_type}")
        logging.info(f"Created: {time_created}")
        logging.info(f"Updated: {updated}")

    except Exception as e:
        # Manejo de errores robusto
        # Si ocurre cualquier error, se registra con logging.error y se relanza
        logging.error(f"Error procesando el archivo: {e}")
        raise