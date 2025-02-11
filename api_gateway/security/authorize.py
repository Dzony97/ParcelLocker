import logging
import jwt
from functools import wraps
from flask import request, current_app, make_response

import logging
logging.basicConfig(level=logging.INFO)


def authorize(roles: list[str] | None = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                header = request.headers.get('Authorization')
                logging.info(header)
                if not header:
                    return make_response({'message': 'Authorization failed - no header'}, 401)

                if not header.startswith(current_app.config['JWT_PREFIX']):
                    return make_response({'message': 'Authorization failed - access token without prefix'}, 401)

                access_token = header.split(' ')[1]

                decoded_access_token = jwt.decode(access_token, current_app.config['JWT_SECRET'], algorithms=[current_app.config['JWT_AUTHTYPE']])
                logging.info('ACCESS TOKEN DATA')
                logging.info(decoded_access_token['role'])
                if roles and decoded_access_token['role'].lower() not in [role.lower() for role in roles]:
                    return make_response({'message': 'Access denied!'}, 403)

            except Exception as error:
                logging.info(repr(error))
                return make_response({'message': 'Authorization failed'}, 401)

            return f(*args, **kwargs)
        return decorated_function
    return decorator