from flask import Flask
from flask_migrate import Migrate
from app.models import db, login
from app.routes import site

def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    login.init_app(app)
    login.login_view = 'login'

    from app.api import api, blueprint, limiter
    from app.api.endpoints import users, todos, register
    from app.api.endpoints.todos import TodosNS
    from app.api.endpoints.users import UserNS
    from app.api.endpoints.register import RegisterNS

    app.register_blueprint(site)
    app.register_blueprint(blueprint)

    limiter.init_app(app)

    api.add_namespace(TodosNS)
    api.add_namespace(UserNS)
    api.add_namespace(RegisterNS)

    return app