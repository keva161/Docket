from flask import Flask, Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from app import api

app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint, doc='/documentation', version='1.0', title='Docket API',
    description='API for Docket. Create users and todo items through a REST API.',
)

app.register_blueprint(blueprint)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app.api.endpoints.todos import TodosNS
from app.api.endpoints.users import UserNS
from app.api.endpoints.register import RegisterNS
from app import routes, models
from app.api.endpoints import users, todos, register

api.add_namespace(TodosNS)
api.add_namespace(UserNS)
api.add_namespace(RegisterNS)