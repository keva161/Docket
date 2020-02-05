from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

login = LoginManager()

def create_app():
    app = Flask(__name__)

    from config import Config

    app.config.from_object(Config)

    db.init_app(app)

    login.init_app(app)
    login.login_view = 'login'

    from app.api import api, blueprint, limiter
    from app.api.endpoints import users, todos, register
    from app.api.endpoints.todos import TodosNS
    from app.api.endpoints.users import UserNS
    from app.api.endpoints.register import RegisterNS

    app.register_blueprint(blueprint)

    limiter.init_app(app)

    api.add_namespace(TodosNS)
    api.add_namespace(UserNS)
    api.add_namespace(RegisterNS)

    return app