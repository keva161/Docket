from logging import StreamHandler
from flask_restplus import Api
from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

blueprint = Blueprint('api', __name__, url_prefix='/api')

limiter = Limiter(key_func=get_remote_address)
limiter.logger.addHandler(StreamHandler())

api = Api(blueprint, doc='/documentation', version='1.0', title='Docket API',
          description='API for Docket. Create users and todo items through a REST API.\n'
                      'First of all, begin by registering a new user via the registration form in the web interface.\n'
                      'Or via a `POST` request to the `/Register/` end point', decorators=[limiter.limit("50/day", error_message="API request limit has been reached (50 per day)")])



