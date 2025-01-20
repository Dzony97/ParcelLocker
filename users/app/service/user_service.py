from dataclasses import dataclass
from app.db.repository import UserRepository, ClientRepository, ActivationTokenRepository
from app.db.entity import ActivationTokenEntity, UserEntity
from app.service.dto import RegisterUserDto, UserDto
from app.mail.configuration import MailSender
from werkzeug.security import generate_password_hash
import datetime
import string
import random


@dataclass
class UserService:
    user_repository: UserRepository
    client_repository: ClientRepository
    activation_token_repository: ActivationTokenRepository

    def register_user(self, register_user_dto: RegisterUserDto, user_dto: UserDto) -> UserDto:

        if not register_user_dto.check_passwords():
            raise ValueError('Passwords is incorrect')

        if self.user_repository.find_by_username(register_user_dto.username):
            raise ValueError('Username is already exists')

        if self.user_repository.find_by_email(register_user_dto.email):
            raise ValueError('Email is already exists')

        user_entity = register_user_dto.with_password(
            generate_password_hash(register_user_dto.password)).to_user_entity()
        self.user_repository.save_or_update(user_entity)
        client_entity = user_dto.to_client_entity(user_entity)
        self.client_repository.save_or_update(client_entity)

        timestamp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=5)
        token = ActivationTokenEntity.generate_token(30)
        user_id = user_entity.id_
        self.activation_token_repository.save_or_update(ActivationTokenEntity(
            timestamp=timestamp.timestamp(),
            token=token,
            user_id=user_id))

        MailSender.send(client_entity.email, 'Activate Your Account', f'<h1>Activation Token: {token}</h1>')

        return UserDto.from_user_entity(user_entity).to_dict()

