import json
import os
from flask import Response, request
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


User_Schema = UserSchema()
Video_Schema = VideoSchema()
Vote_Schema= VoteSchema()
VideoLeaderboard_Schema = VideoLeaderboardSchema()
UPLOAD_FOLDER = 'videos'
PROCESSED_FOLDER = 'videos'




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
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            video_url = f'http://example.com/{filename}'
            output_path = os.path.join(PROCESSED_FOLDER, f"processed_{filename}")
            video_url_proc = f'http://example.com/processed{filename}'
     
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
            print(new_video.title,file_path, output_path, 20)
            
            process_video.delay(new_video.title,file_path, output_path, 20)
            db.session.add(new_video)
            db.session.commit()
        
            return Response('Vídeo subido y proceso iniciado correctamente', status=201, headers={'video_url': video_url})
    
        else:
            return Response('El tipo de archivo no está permitido', status=400)
        
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'jpg', 'png'}

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
        if video is None:
            return Response(response=json.dumps({'message': 'Video no encontrado o no tienes permiso para acceder a este video.'}), status=404, mimetype='application/json')

        filename_original = os.path.basename(video.url_original)
        filename_processed = os.path.basename(video.url_processed)

        try:
            db.session.delete(video)
            db.session.commit()
            os.remove(os.path.join(UPLOAD_FOLDER, filename_original))
            os.remove(os.path.join(PROCESSED_FOLDER, filename_processed))

            return {'message': 'Video eliminado exitosamente'}, 200
        except Exception as e:
            return {'message': 'Error al eliminar el video'}, 500
    
    

def procesar_video(input_path, output_path, duracion_maxima):
    video = VideoFileClip(input_path)
    video_recortado = video.subclip(0, duracion_maxima)
    video_recortado.write_videofile(output_path)
    video.close()
    video_recortado.close()
    
