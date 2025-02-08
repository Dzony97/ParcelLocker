import logging
import jwt
from functools import wraps
from flask import request, current_app, make_response


def authorize(roles: list[str] | None = None):
    roles = roles or []

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                header = request.headers.get('Authorization')
                if not header:
                    return make_response({'message': 'Authorization failed - no header'}, 401)

                jwt_prefix = current_app.config.get('JWT_PREFIX', 'Bearer')
                if not header.startswith(jwt_prefix):
                    return make_response({'message': 'Authorization failed - access token without prefix'}, 401)

                access_token = header.split(' ')[1]

                secret = current_app.config['JWT_SECRET']
                algorithm = current_app.config['JWT_AUTHTYPE']
                decoded_access_token = jwt.decode(access_token, secret, algorithms=[algorithm])

                user_role = decoded_access_token.get('role')
                logging.info(f"Użytkownik o roli: {user_role}")

                if roles and user_role.lower() not in [r.lower() for r in roles]:
                    return make_response({'message': 'Access denied!'}, 403)

            except Exception as error:
                logging.error(repr(error))
                return make_response({'message': 'Authorization failed'}, 401)

            return f(*args, **kwargs)
        return decorated_function
    return decorator