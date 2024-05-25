from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaLogIn, VistaSignIn, vistaTasks, VistaTask
import os

app = create_app('default')

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/api/auth/singup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(vistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/task/<int:id>')

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)