from flask import Flask, Blueprint, request, make_response, current_app
from functools import wraps
from werkzeug.security import check_password_hash
from app.db.entity import UserEntity
from app.db.repository import user_repository
from app.config import JWT_CONFIG
import datetime
import jwt
import logging
logger = logging.basicConfig(level=logging.INFO)


def configure_security(app: Flask) -> None:
    @app.route('/login', methods=['POST'])
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
            'sub': user.id_,
        }

        refresh_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': refresh_token_exp,
            'sub': user.id_,
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