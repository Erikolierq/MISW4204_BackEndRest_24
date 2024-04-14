import json
from flask import Response, request
from sqlalchemy import exc
from ..modelos import db, User, UserSchema, Video, VideoSchema, Vote, VoteSchema, VideoLeaderboard, VideoLeaderboardSchema
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from celery import Celery


User_Schema = UserSchema()
Video_Schema = VideoSchema()
Vote_Schema= VoteSchema()
VideoLeaderboard_Schema = VideoLeaderboardSchema()

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
        tasks = Video.query.filter(User.id == current_user.id)
        return User_Schema.dump(tasks, many=True)
    
    @jwt_required()
    def post(self):
        pass

class VistaTask(Resource):
    @jwt_required()
    def get(self):
        pass
     
    @jwt_required()
    def delete(self):
        pass    