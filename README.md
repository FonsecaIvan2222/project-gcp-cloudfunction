# Proyecto Cloud Function en GCP

## Descripción
Este proyecto implementa una **Cloud Function en Google Cloud Platform (GCP)** que se activa automáticamente al subir archivos a un bucket de Cloud Storage.  
La función tiene como objetivo extraer **metadatos del archivo** (nombre, tamaño, tipo, fechas y versión) y registrar los eventos en **Cloud Logging**, con manejo robusto de errores y registros detallados para facilitar la depuración.  

Este proyecto sirve como prueba de conceptos para automatización en la nube, control de versiones de archivos, gestión de permisos y monitoreo de eventos mediante Cloud Functions y Cloud Logging.

---

## Tabla de Contenido
1. [Creación y Configuración del Proyecto](#creación-y-configuración-del-proyecto)
2. [Diseño de Almacenamiento y Automatización](#diseño-de-almacenamiento-y-automatización)
3. [Cloud Function](#cloud-function)
4. [Pruebas y Verificación](#pruebas-y-verificación)
5. [Estructura del Repositorio](#estructura-del-repositorio)
6. [Comentarios en el Código](#comentarios-en-el-código)
7. [Capturas y Diagramas](#capturas-y-diagramas)
8. [Conclusiones y Observaciones](#conclusiones-y-observaciones)

---

## Creación y Configuración del Proyecto
En esta fase se estableció la base del proyecto:

- Se creó un proyecto nuevo en GCP, con un nombre descriptivo para facilitar su identificación en la consola.
- Se habilitaron las siguientes **APIs esenciales**:
  - **Cloud Storage**: Para la gestión de buckets y almacenamiento de archivos.
  - **Cloud Functions**: Para la ejecución de funciones en respuesta a eventos.
  - **Cloud Pub/Sub**: Para comunicación basada en eventos (opcional, si se requiere mensajería).
  - **Cloud Logging**: Para registrar eventos y depuración de la Cloud Function.
  - **Cloud Build**: Opcional, para despliegue y automatización continua de la función.

> Nota: Cada API se habilitó desde la sección de "APIs y Servicios" en la consola de GCP.  
> Se recomienda capturar la pantalla de la sección de APIs habilitadas para documentación.

- **Roles y permisos IAM**:
  - Usuario de prueba: `ivancancer007@gmail.com`
  - Permisos asignados: únicamente lectura y escritura, simulando un entorno controlado de producción.
  - Este usuario permitió validar que los permisos fueran correctos sin comprometer el proyecto principal.

---

## Diseño de Almacenamiento y Automatización
En esta fase se estableció la estructura de almacenamiento y las reglas para automatización de archivos:

- **Bucket creado:** `bucketpruebaturing`  
- **Ubicación / región:** Se seleccionó una región específica para evitar problemas de latencia y compatibilidad con Cloud Functions.
- **Reglas de ciclo de vida (lifecycle):**
  - **Antigüedad:** 30 días → Los archivos que superen este tiempo se eliminan automáticamente.
  - **Cantidad de versiones anteriores:** 4 → Se mantiene un historial de las últimas 4 versiones de cada archivo.
  - **Tiempo personalizado:** 4 días → Permite establecer reglas específicas de retención que complementan la antigüedad y cantidad de versiones.
  
> Justificación: Estas reglas aseguran la limpieza automática del bucket, control de versiones y ahorro de espacio, evitando acumulación de archivos antiguos o versiones innecesarias.

- **Políticas de acceso refinadas:**
  - Usuario `ivancancer007@gmail.com` con permisos **de lectura y escritura**.
  - No se otorgaron permisos administrativos ni de eliminación global para mantener la seguridad.

---

## Cloud Function
En esta fase se desarrolló y desplegó la función que automatiza la extracción de metadatos:

- **Lenguaje:** Python 3.11
- **Trigger:** Cloud Storage → Evento `Finalize/Create` (cuando se sube un archivo)
- **Funcionalidad:**
  - Extrae metadatos de los archivos subidos:
    - Nombre
    - Tamaño en bytes
    - Tipo de contenido
    - Fechas de creación y actualización
    - Versión (`metageneration`)
  - Registra toda la información en **Cloud Logging**.
  - Incluye **manejo robusto de errores**, para capturar excepciones y registrar fallos.
  
- **Revisión de implementación:** Cada despliegue genera automáticamente una revisión en GCP, permitiendo:
  - Mantener historial de versiones
  - Facilitar rollback a versiones anteriores
  - Auditar cambios y trazabilidad de eventos

### Código de la Cloud Function (`main.py`):

```python
import functions_framework
import logging

@functions_framework.cloud_event
def metadata(cloud_event):
    try:
        data = cloud_event.data

        event_id = cloud_event["id"]
        event_type = cloud_event["type"]

        bucket = data.get("bucket")
        name = data.get("name")
        metageneration = data.get("metageneration")
        size = data.get("size")
        content_type = data.get("contentType")
        time_created = data.get("timeCreated")
        updated = data.get("updated")

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
        logging.error(f"Error procesando el archivo: {e}")
        raise
