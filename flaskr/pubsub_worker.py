from celery import Celery
from google.cloud import pubsub_v1
import json
from moviepy.editor import VideoFileClip
import os
from google.cloud import storage

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
path1 = 'claves\soluciones-cloud-420823-70ce317b34ee.json'
path2 = 'flaskr\claves\soluciones-cloud-420823-70ce317b34ee.json'

def file_exists(path):
    return os.path.isfile(path)

# Verificar si el archivo existe en la primera ruta
if file_exists(path1):
    credentials_path = path1
# Si no existe en la primera ruta, verificar en la segunda ruta
elif file_exists(path2):
    credentials_path = path2
else:
    # Si no se encuentra en ninguna de las rutas
    print("El archivo no se encuentra en ninguna de las ubicaciones especificadas")

    
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
storage_client = storage.Client()
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('soluciones-cloud-420823', 'process-video-subscription')

def upload_to_gcs(file_path, bucket_name, destination_blob_name):
    #Sube un archivo a un bucket de Google Cloud Storage.
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    os.remove(file_path)
    print(f"Archivo {file_path} subido a {destination_blob_name} en el bucket {bucket_name}.")

def callback(message):
    data = json.loads(message.data.decode('utf-8'))
    filename = data['filename']
    input_path = data['file_path']
    output_path = data['output_path']
    duracion_maxima = data['duracion_maxima']
    
    video = VideoFileClip(input_path)
    video_recortado = video.subclip(0, duracion_maxima)
    video_recortado.write_videofile(output_path)
    video.close()
    video_recortado.close()

    upload_to_gcs(output_path, "backmisw4204", f"editado/{os.path.basename(output_path)}")
    upload_to_gcs(input_path, "backmisw4204", f"original/{filename}")

    message.ack()
    
# Suscribirse al Pub/Sub topic
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..")

# Mantener el proceso en ejecución
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    streaming_pull_future.result()
