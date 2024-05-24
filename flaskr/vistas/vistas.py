import json
import os
from flask import Response, request,Flask
from sqlalchemy import exc
from ..modelos import db, User, UserSchema, Video, VideoSchema, Vote, VoteSchema, VideoLeaderboard, VideoLeaderboardSchema
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from celery import Celery
from datetime import datetime
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
from flask import abort
from ..modelos.tareas import process_video
from flask import current_app
from google.cloud import storage
from google.oauth2 import service_account
from urllib.parse import urlparse

#with open('claves\soluciones-cloud-420823-70ce317b34ee.json') as f:
    #credentials_data = json.load(f)
User_Schema = UserSchema()
Video_Schema = VideoSchema()
Vote_Schema= VoteSchema()
VideoLeaderboard_Schema = VideoLeaderboardSchema()
UPLOAD_FOLDER = 'videos'
PROCESSED_FOLDER = 'videos'
#service_account_key = credentials_data['private_key']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'claves\clave.json'
#credentials = service_account.Credentials.from_service_account_file(
    #'claves\soluciones-cloud-420823-70ce317b34ee.json'
#)
#client = storage.Client(credentials=credentials)




class VistaSignIn(Resource):

    def post(self):
        new_user = User(username=request.json['username'], email=request.json['email'], password=request.json['password'])
        db.session.add(new_user)
        try:
            db.session.commit()
        except exc.IntegrityError:
            return Response(response=json.dumps({"error": "El usuario ya existe"}), status=400, mimetype='application/json')
        return User_Schema.dump(new_user)


class VistaLogIn(Resource):
    
    def post(self):
        usuario = User.query.filter(User.username == request.json["username"],
                                       User.password == request.json["password"]).first()
        if usuario is None:
            return "Verifique los datos ingresados", 404
        token_de_acceso = create_access_token(identity=usuario.id)
        return {"mensaje": "Inicio de sesion exitoso", "token": token_de_acceso}
    
class vistaTasks(Resource):
    
    @jwt_required()
    def get(self):
        videos = Video.query.filter_by(user_id=current_user.id).all()
        video_data = [{
            'id': video.id,
            'title': video.title,
            'processed': video.processed,
            'url_procesada': video.url_processed,
            'url_original': video.url_original
        } for video in videos]
        response_data = {'videos': video_data}
        return Response(response=json.dumps(response_data), status=200, mimetype='application/json')
    
    @jwt_required()
    def post(self):
        if 'file' not in request.files:
            return Response('No se proporcionó ningún archivo', status=400)
        
        file = request.files['file']
    
        if file.filename == '':
            return Response('No se seleccionó ningún archivo', status=400)
    
        if file and allowed_file(file.filename):
            total_videos = str(Video.query.count())
            filename = secure_filename(total_videos+file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            video_url = f'https://storage.cloud.google.com/backmisw4204/original/{filename}'
            output_path = os.path.join(PROCESSED_FOLDER, f"processed_{filename}")
            video_url_proc = f'https://storage.cloud.google.com/backmisw4204/editado/processed_{filename}'
     
            new_video = Video(
                title=request.form.get('title'),
                description=request.form.get('description'),
                url_original=video_url,
                url_processed=video_url_proc, 
                uploaded_at=datetime.utcnow(),
                processed="upload",  
                user_id=current_user.id
            )
            file_path="flaskr/"+file_path
            output_path="flaskr/"+output_path
            
            print(filename,file_path, output_path, 20)
            
            process_video.delay(filename,file_path, output_path, 20, total_videos)
            db.session.add(new_video)
            db.session.commit()
        
            return Response('Vídeo subido y proceso iniciado correctamente', status=201, headers={'video_url': video_url})
    
        else:
            return Response('El tipo de archivo no está permitido', status=400)
        
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}
    
class VistaTask(Resource):
    @jwt_required()
    def get(self, id):
        video = Video.query.filter_by(id=id).first()
        if video is None:
            return Response(response=json.dumps({'message': 'Video no encontrado o no tienes permiso para acceder a este video.'}), status=404, mimetype='application/json')
        response_data = {
            'id': video.id,
            'title': video.title,
            'processed': video.processed,
            
        }
        if video.processed == 'processed':
            response_data['url_procesada'] = video.url_processed
        return Response(response=json.dumps(response_data), status=200, mimetype='application/json')
     
    @jwt_required()
    def delete(self, id):
        video = Video.query.filter_by(id=id).first()
        print(video.title)
        if video is None:
            return Response(response=json.dumps({'message': 'Video no encontrado o no tienes permiso para acceder a este video.'}), status=404, mimetype='application/json')

        url_original = video.url_original
        url_procesada = video.url_processed
        print(url_original)
        print(url_procesada)
        try:
            db.session.delete(video)
            db.session.commit()
            
            delete_blob_from_url(url_procesada)
            delete_blob_from_url(url_original)

            return {'message': 'Video eliminado exitosamente'}, 200
        except Exception as e:
            return {'message': 'Error al eliminar el video'}, 500
    
    

def delete_blob_from_url(url):
    
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    
    bucket_name = path_parts[1]
    blob_name = '/'.join(path_parts[2:])
    
    delete_blob(bucket_name, blob_name)

def delete_blob(bucket_name, blob_name):
    
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print(f"Blob {blob_name} deleted.")
