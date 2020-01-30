from flask_restplus import fields
from app import api

UserModel = api.model('User', {'Username': fields.String(), 'Email Address': fields.String(), 'Password': fields.String()})

TodoModel = api.model('Todo', {'Body': fields.String()})