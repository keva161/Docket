import os
basedir = os.path.dirname(__file__)

class Config(object):
    SECRET_KEY = 'NOT_SO_SECRET'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False