from flask import Flask, Blueprint, request, make_response, current_app
from functools import wraps
from werkzeug.security import check_password_hash
from app.db.entity import UserEntity
from app.config import (
    JWT_ISSUER,
    JWT_AUTHTYPE,
    JWT_SECRET,
    JWT_ACCESS_MAX_AGE,
    JWT_REFRESH_MAX_AGE,
    JWT_PREFIX
)
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

        user = UserEntity.find_by_username(username)

        if not user:
            return make_response({'message': 'Authentication - user not found'}, 400)

        if not user.active:
            return make_response({'message': 'Authentication - user is not active'}, 500)

        if not user.check_password(password):
            return make_response({'message': 'Authentication - password is not correct'}, 400)