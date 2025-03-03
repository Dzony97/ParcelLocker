from dataclasses import dataclass
from app.db.repository import UserRepository, ClientRepository, ActivationTokenRepository
from app.db.entity import ActivationTokenEntity, UserEntity
from app.service.dto import RegisterUserDto, UserDto
from app.mail.configuration import MailSender
from app.config import (
    ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS,
    ACTIVATION_TOKEN_LENGTH
)
from werkzeug.security import generate_password_hash
import datetime


@dataclass
class UserService:
    """
    Service for handling user-related business logic such as registration, activation, and user retrieval.

    Attributes:
        user_repository (UserRepository): Repository for managing User entities.
        client_repository (ClientRepository): Repository for managing Client entities.
        activation_token_repository (ActivationTokenRepository): Repository for managing activation tokens.
    """

    user_repository: UserRepository
    client_repository: ClientRepository
    activation_token_repository: ActivationTokenRepository

    def register_user(self, register_user_dto: RegisterUserDto, user_dto: UserDto) -> UserDto:
        """
        Registers a new user by validating the provided registration data, saving the user and associated client,
        generating an activation token, and sending the token to the user's email.

        Args:
            register_user_dto (RegisterUserDto): DTO containing the registration data.
            user_dto (UserDto): DTO containing user-related data for creating a client entity.

        Returns:
            UserDto: The registered user DTO with user data.

        Raises:
            ValueError: If passwords do not match, username or email already exists, or other validation fails.
        """
        if not register_user_dto.check_passwords():
            raise ValueError('Passwords do not match')

        if self.user_repository.find_by_username(register_user_dto.username):
            raise ValueError('Username already exists')

        if self.user_repository.find_by_email(register_user_dto.email):
            raise ValueError('Email already exists')

        user_entity = register_user_dto.with_password(
            generate_password_hash(register_user_dto.password)).to_user_entity()

        self.user_repository.save_or_update(user_entity)

        client_entity = user_dto.to_client_entity(user_entity)
        self.client_repository.save_or_update(client_entity)

        timestamp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            seconds=ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS)
        token = ActivationTokenEntity.generate_token(ACTIVATION_TOKEN_LENGTH)
        user_id = user_entity.id_

        self.activation_token_repository.save_or_update(ActivationTokenEntity(
            timestamp=timestamp.timestamp(),
            token=token,
            user_id=user_id))

        MailSender.send(client_entity.email, 'Activate Your Account', f'<h1>Activation Token: {token}</h1>')

        return UserDto.from_user_entity(user_entity).to_dict()

    def activate_user(self, token: str) -> UserDto:
        """
        Activates a user account using the provided activation token. The token is validated, and the user is
        activated if the token is valid and not expired.

        Args:
            token (str): The activation token sent to the user.

        Returns:
            UserDto: The activated user DTO.

        Raises:
            ValueError: If the token is invalid or expired.
        """
        activation_token_with_user = self.activation_token_repository.find_by_token(token)

        if activation_token_with_user is None:
            raise ValueError('User not found')

        if not activation_token_with_user.is_active():
            raise ValueError('Token has expired')

        self.activation_token_repository.delete_by_id(activation_token_with_user.id_)

        user_to_activate = activation_token_with_user.user
        user_to_activate.is_active = True
        self.user_repository.save_or_update(user_to_activate)

        return UserDto.from_user_entity(user_to_activate).to_dict()
