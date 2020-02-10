from app import db
from flask_restplus import Resource, Namespace
from app.models import User
from app.api.models import UserModel
from flask import jsonify, request, make_response
import uuid
#from app import limiter

RegisterNS = Namespace('Register', description='Register for the application')


@RegisterNS.route('/')
class Register(Resource):
    #decorators = [limiter.limit('50 per day')]

    @RegisterNS.expect(UserModel)
    def post(self):
        """Creates a new user and returns an API token."""
        data = request.get_json()

        if not data:
            return jsonify({'message': 'Please enter some user data'})
        else:
            user = User(api_token=str(uuid.uuid4()), username=data['Username'], email=data['Email Address'])
            if data["Password"] != type(str):
                jsonify({'message' : 'Password needs to be a string'})
            else:
                user.set_password(data['Password'])
            try:
                db.session.add(user)
                print("Registering a new user")
                db.session.commit()
                return jsonify({'message': "New user created! Token: " + user.api_token})
            except Exception as e:
                print(e)
                db.session.rollback()
                return {'Message': 'Username or email address is invalid!'}
