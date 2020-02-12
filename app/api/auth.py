from flask import request
from functools import wraps
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Token' in request.headers:
            token = request.headers['Token']
            valid_user = User.query.filter_by(api_token=token).first()
            if not valid_user:
                return {'message': 'Token is invalid or missing'}
        else:
            return {'message': 'Token is invalid or missing'}

        return f(*args, **kwargs)

    return decorated
