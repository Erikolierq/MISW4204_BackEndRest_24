from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaLogIn, VistaSignIn, vistaTasks, VistaTask

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/api/auth/singup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(vistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id>')

