from app import db
from flask_restplus import Resource, Namespace
from app.models import User
from app.api.models import UserModel
from app.api.auth import token_required
from flask import jsonify, request
import uuid

UserNS = Namespace('Users', description='User related operations')

@UserNS.route('/')
class Users(Resource):
    @token_required
    def get(self):
        """Returns list of registered users."""
        output = []
        users = User.query.all()
        for user in users:
            output.append({'username': user.username, 'email': user.email})
        return jsonify(output)

    @token_required
    def delete(self):
        """Deletes the user with the associated API token."""
        token = request.headers['Token']
        try:
            User.query.filter_by(api_token=token).delete()
            db.session.commit()
            return jsonify({'message': 'Current user deleted'})
        except:
            db.session.rollback()
            return jsonify({'message': 'Invalid user'})

    @UserNS.expect(UserModel)
    @token_required
    def put(self):
        """Updates the user details associated with the API token."""
        token = request.headers['Token']
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Please enter some user data'})
        else:
            update_user = User.query.filter_by(api_token=token).first()

            try:
                update_user.username = data["Username"]
                update_user.email = data['Email Address']
                update_user.set_password(data['Password'])
                db.session.commit()
                return {'Message': 'Record updated!'}
            except:
                return {'Message': 'Username or email address is invalid!'}
