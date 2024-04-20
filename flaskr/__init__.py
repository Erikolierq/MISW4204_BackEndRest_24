from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .modelos import db, User
from celery import Celery

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

def make_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(config_name):
    app = Flask(__name__)  
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IDRL.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config["JWT_SECRET_KEY"] = "frase-secreta"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app_context = app.app_context()
    app_context.push()
    CORS(app)

    jwt = JWTManager(app)
    celery = make_celery(app)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()
    
    
    
    return app