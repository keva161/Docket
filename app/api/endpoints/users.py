from app.models import db, User, Todo
from flask_restplus import Resource, Namespace
from flask import jsonify, request
from app.api.models import UserModel
from app.api.auth import token_required

UserNS = Namespace('Users', description='User related operations')

@UserNS.route('/')
class Users(Resource):
    @token_required
    def get(self):
        """Returns list of registered users."""
        output = []
        users = User.query.all()
        if not users:
            print("There are no registered users to deliver")
            return jsonify({'message' : 'There are no registered users'})
        else:
            for user in users:
                print("Delivering a list of registered users")
                output.append({'username': user.username, 'email': user.email})
            return jsonify(output)

    @token_required
    def delete(self):
        """Deletes the user with the associated API token."""
        token = request.headers['Token']
        user = User.query.filter_by(api_token=token).first()
        try:
            db.session.query(User).filter_by(api_token=token).delete()
            db.session.query(Todo).filter_by(user_id=user.id).delete()
            db.session.commit()
            print("Deleted a registered user")
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
            print("Updating user details")
            if data["Password"] != type(str):
                jsonify({'message' : 'Password needs to be a string'})
            else:
                update_user.username = data["Username"]
                update_user.email = data['Email Address']
                update_user.set_password(data['Password'])
            try:
                db.session.commit()
                return {'Message': 'Record updated!'}
            except Exception as e:
                print(e)
                return {'Message': 'Username or email address is invalid!'}
