from dataclasses import dataclass
from app.db.repository import UserRepository
from app.service.dto import RegisterUserDto, UserDto


@dataclass
class UserService:
    user_repository: UserRepository

    def register_user(self, register_user_dto: RegisterUserDto) -> UserDto:

        if not register_user_dto.check_passwords():
            raise ValueError('Passwords is incorrect')

        if self.user_repository.find_by_username(register_user_dto.username):
            raise ValueError('Username is already exists')

        if self.user_repository.find_by_email(register_user_dto.email):
            raise ValueError('Email is already exists')

        user_entity = register_user_dto.with_password(register_user_dto.password).to_user_entity()
        self.user_repository.save_or_update(user_entity)

        return UserDto.from_user_entity(user_entity).to_dict()
