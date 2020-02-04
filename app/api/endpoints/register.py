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
            user.set_password(data['Password'])
            try:
                db.session.add(user)
                db.session.commit()
                return jsonify({'message': 'New user created! : Your API token is ' + user.api_token})
            except:
                db.session.rollback()
                return {'Message': 'Username or email address is invalid!'}
