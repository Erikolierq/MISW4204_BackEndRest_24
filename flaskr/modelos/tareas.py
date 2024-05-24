from celery import Celery
import time
from .modelos import Video,db
from moviepy.editor import VideoFileClip
import os
from google.cloud import storage

path1 = 'claves/clave.json'
path2 = 'flaskr/claves/clave.json'

def file_exists(path):
    return os.path.isfile(path)

# Verificar si el archivo existe en la primera ruta
if file_exists(path1):
    credentials_path = path1
# Si no existe en la primera ruta, verificar en la segunda ruta
elif file_exists(path2):
    credentials_path = path2
else:
    # Si no se encuentra en ninguna de las rutas, mostrar un mensaje de error o manejarlo según lo necesites
    print("El archivo no se encuentra en ninguna de las ubicaciones especificadas")

    
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path    
celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
storage_client = storage.Client()

@celery.task(bind=True)
def process_video(self,video_title,input_path, output_path, duracion_maxima, total_videos):
    
    video = VideoFileClip(input_path)
    video_recortado = video.subclip(0, duracion_maxima)
    video_recortado.write_videofile(output_path)
    video.close()
    video_recortado.close()
    filename = os.path.basename(total_videos+output_path)
    
    # Subir el video procesado a GCS
    upload_to_gcs(output_path, "backmisw4204", f"editado/{filename}")

    # Subir el video original a GCS
    upload_to_gcs(input_path, "backmisw4204", f"original/{video_title}")
    

def upload_to_gcs(file_path, bucket_name, destination_blob_name):
    """Sube un archivo a un bucket de Google Cloud Storage."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    os.remove(file_path)
    print(f"Archivo {file_path} subido a {destination_blob_name} en el bucket {bucket_name}.")
    