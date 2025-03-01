from flask_restful import Resource, reqparse
from flask import Response, jsonify, make_response
from app.db.repository import UserRepository
from app.db.entity import UserEntity
from app.service.dto import RegisterUserDto, UserDto
from app.service.configuration import user_service
import logging

logging.basicConfig(level=logging.INFO)


class RegisterUserResource(Resource):
    """
    Resource for handling user registration requests.

    Methods:
        post() -> Response: Handles POST requests to register a new user.
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username cannot be empty')
    parser.add_argument('email', type=str, required=True, help='Email cannot be empty')
    parser.add_argument('password', type=str, required=True, help='Password cannot be empty')
    parser.add_argument('password_confirmation', type=str, required=True, help='Password confirmation cannot be empty')
    parser.add_argument('phone_number', type=str, required=True, help='Phone number cannot be empty')
    parser.add_argument('first_name', type=str, required=True, help='Firstname cannot be empty')
    parser.add_argument('last_name', type=str, required=True, help='Lastname cannot be empty')
    parser.add_argument('role', type=str, required=True, help='Role cannot be empty')

    def post(self) -> Response:
        """
        Handles POST requests to register a new user.

        Retrieves user registration data from the request body, validates the input,
        and passes it to the `user_service.register_user` method for registration.

        Returns:
            Response: The result of the registration process (success or failure).
        """
        register_user_dto = RegisterUserDto.from_dict(RegisterUserResource.parser.parse_args())
        return user_service.register_user(register_user_dto, UserDto)


class ActivationUserResource(Resource):
    """
    Resource for handling user activation requests using a token.

    Methods:
        post() -> Response: Handles POST requests to activate a user account.
    """

    parser = reqparse.RequestParser()
    parser.add_argument('token', type=str, required=True, help='Token cannot be empty')

    def post(self) -> Response:
        """
        Handles POST requests to activate a user account using a token.

        Retrieves the token from the request body and passes it to `user_service.activate_user`
        for user account activation.

        Returns:
            Response: The result of the user activation process (success or failure).
        """
        json_body = ActivationUserResource.parser.parse_args()
        return user_service.activate_user(json_body['token'])
