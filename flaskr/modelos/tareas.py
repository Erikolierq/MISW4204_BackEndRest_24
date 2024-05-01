from celery import Celery
import time
from .modelos import Video,db
from moviepy.editor import VideoFileClip
import os



celery = Celery(__name__, broker='redis://10.138.0.29:6379/0', backend='redis://10.138.0.29:6379/0')




@celery.task(bind=True)
def process_video(self,video_title,input_path, output_path, duracion_maxima):
    
    video = VideoFileClip(input_path)
    video_recortado = video.subclip(0, duracion_maxima)
    video_recortado.write_videofile(output_path)
    video.close()
    video_recortado.close()

    filename = os.path.basename(output_path)
    processed_video_url = f'http://example.com/processed{filename}'
    video = Video.query.filter_by(title=video_title).first()
    if video is not None:
        video.url_processed = processed_video_url
        video.processed = "processed"
        db.session.commit()
    else:
        print("No se encontró ningún video con el título:", video_title)
    