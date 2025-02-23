from flask import Flask, Blueprint, request, make_response, current_app
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from functools import wraps
from werkzeug.security import check_password_hash
from app.db.entity import UserEntity
from app.db.repository import user_repository
from app.config import JWT_CONFIG
import datetime
import jwt
import logging
logger = logging.basicConfig(level=logging.INFO)

users_blueprint = Blueprint('users', __name__, url_prefix='/users')

def configure_security(app: Flask) -> None:
    @users_blueprint.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = user_repository.find_by_username(username)

        if not user:
            return make_response({'message': 'Authentication - user not found'}, 400)

        if not user.is_active:
            return make_response({'message': 'Authentication - user is not active'}, 500)

        if not user.check_password(password):
            return make_response({'message': 'Authentication - password is not correct'}, 400)

        access_token_exp = int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=app.config['JWT_ACCESS_MAX_AGE'])).timestamp())
        refresh_token_exp = int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=app.config['JWT_REFRESH_MAX_AGE'])).timestamp())

        access_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': access_token_exp,
            'sub': str(user.id_),
            'role': user.role,
        }

        refresh_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': refresh_token_exp,
            'sub': str(user.id_),
            'role': user.role,
            'access_token_exp': access_token_exp
        }

        access_token = jwt.encode(access_token_payload, app.config['JWT_SECRET'], algorithm=app.config['JWT_AUTHTYPE'])
        refresh_token = jwt.encode(refresh_token_payload, app.config['JWT_SECRET'], algorithm=app.config['JWT_AUTHTYPE'])

        response_body = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        response = make_response(response_body, 201)

        response.headers['Access-Token'] = access_token
        response.headers['Refresh-Token'] = refresh_token

        response.set_cookie('AccessToken', access_token, httponly=True)
        response.set_cookie('RefreshToken', refresh_token, httponly=True)

        return response

    @users_blueprint.route('/refresh', methods=['POST'])
    def refresh():
        request_data = request.get_json()
        refresh_token = request_data.get('token')

        if not refresh_token:
            return make_response({'message': 'Token is missing'}, 400)

        try:
            decoded_refresh_token = jwt.decode(
                refresh_token,
                app.config['JWT_SECRET'],
                algorithms=[app.config['JWT_AUTHTYPE']]
            )

            if decoded_refresh_token['access_token_exp'] < datetime.datetime.now(datetime.UTC).timestamp():
                return make_response({'message': 'Cannot refresh token - access token has been expired'}, 401)

            new_access_token_exp = int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(
                minutes=app.config['JWT_ACCESS_MAX_AGE'])).timestamp())

            access_token_payload = {
                'iat': datetime.datetime.now(datetime.UTC),
                'exp': new_access_token_exp,
                'sub': str(decoded_refresh_token['sub']),
                'role': decoded_refresh_token['role'],
            }

            refresh_token_payload = {
                'iat': datetime.datetime.now(datetime.UTC),
                'exp': decoded_refresh_token['exp'],
                'sub': decoded_refresh_token['sub'],
                'role': decoded_refresh_token['role'],
                'access_token_exp': new_access_token_exp
            }

            access_token = jwt.encode(access_token_payload, app.config['JWT_SECRET'],
                                      algorithm=app.config['JWT_AUTHTYPE'])
            refresh_token = jwt.encode(refresh_token_payload, app.config['JWT_SECRET'],
                                       algorithm=app.config['JWT_AUTHTYPE'])

            response_body = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            response = make_response(response_body, 201)

            response.headers['Access-Token'] = access_token
            response.headers['Refresh-Token'] = refresh_token

            response.set_cookie('AccessToken', access_token, httponly=True)
            response.set_cookie('RefreshToken', refresh_token, httponly=True)

            return response

        except ExpiredSignatureError:
            return make_response({'message': 'Cannot refresh token - refresh token has expired'}, 401)
        except (DecodeError, InvalidTokenError):
            return make_response({'message': 'Invalid refresh token'}, 401)
        except Exception as e:
            return make_response({'message': f'Unexpected error: {str(e)}'}, 500)