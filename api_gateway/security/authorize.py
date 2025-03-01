import logging
import jwt
from functools import wraps
from flask import request, current_app, make_response

import logging

logging.basicConfig(level=logging.INFO)


def authorize(roles: list[str] | None = None):
    """
    Decorator to enforce authorization based on JWT token and optional role-based access control.

    This decorator checks if the request contains a valid JWT token in the 'Authorization' header.
    It also ensures that the decoded token contains an appropriate role if the 'roles' parameter is provided.

    :param roles: List of roles that are allowed to access the route. If None, any valid token is allowed.
    :return: The decorated function is only called if authorization is successful, otherwise, an error response is returned.
    """

    def decorator(f):
        """
        The actual decorator that wraps the route handler function.

        This function performs the JWT validation and role checking. If the token is valid and the
        user's role matches the allowed roles (if provided), the route handler is executed. Otherwise,
        a 401 Unauthorized or 403 Forbidden error is returned.

        :param f: The route handler function to be wrapped by the decorator.
        :return: The route handler function is called if authorization passes, otherwise an error response is returned.
        """

        @wraps(f)
        def decorated_function(*args, **kwargs):
            """
            This function is responsible for handling the incoming request and performing the
            authorization checks before calling the wrapped route handler.

            It extracts the JWT token from the 'Authorization' header, decodes it, and checks if the
            decoded token contains a valid role (if applicable). If any of the checks fail, it returns
            an error response.

            :param args: Positional arguments passed to the route handler.
            :param kwargs: Keyword arguments passed to the route handler.
            :return: The result of the route handler function if authorization passes, otherwise an error response.
            """
            try:
                header = request.headers.get('Authorization')
                logging.info(header)

                if not header:
                    return make_response({'message': 'Authorization failed - no header'}, 401)

                if not header.startswith(current_app.config['JWT_PREFIX']):
                    return make_response({'message': 'Authorization failed - access token without prefix'}, 401)

                access_token = header.split(' ')[1]

                decoded_access_token = jwt.decode(access_token, current_app.config['JWT_SECRET'],
                                                  algorithms=[current_app.config['JWT_AUTHTYPE']])
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
