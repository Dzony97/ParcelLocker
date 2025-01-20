from flask_restful import Resource, reqparse
from flask import Response, jsonify, make_response
from app.db.repository import UserRepository
from app.db.entity import UserEntity
from app.service.dto import RegisterUserDto, UserDto
from app.service.configuration import user_service
import logging

logging.basicConfig(level=logging.INFO)


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username cannot be empty')
    parser.add_argument('email', type=str, required=True, help='Email cannot be empty')
    parser.add_argument('password', type=str, required=True, help='Password cannot be empty')
    parser.add_argument('password_confirmation', type=str, required=True, help='Password confirmation cannot be empty')
    parser.add_argument('phone_number', type=str, required=True, help='Phone number cannot be empty')
    parser.add_argument('first_name', type=str, required=True, help='Firstname cannot be empty')
    parser.add_argument('last_name', type=str, required=True, help='Lastname cannot be empty')

    def post(self) -> Response:
        register_user_dto = RegisterUserDto.from_dict(UserResource.parser.parse_args())
        return user_service.register_user(register_user_dto, UserDto)

    
class ActivationUserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('token', type=str, required=True, help='Token cannot be empty')

    def post(self) -> Response:
        json_body = ActivationUserResource.parser.parse_args()
        return user_service.activate_user(json_body['token'])