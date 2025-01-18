from dataclasses import dataclass
from app.db.entity import UserEntity, ClientEntity
from typing import Self


@dataclass
class RegisterUserDto:
    username: str
    password: str
    password_confirmation: str
    email: str
    phone_number: str
    first_name: str
    last_name: str

    def check_passwords(self) -> bool:
        return self.password == self.password_confirmation

    def with_password(self, new_password: str) -> Self:
        return RegisterUserDto(
            username=self.username,
            email=self.email,
            password=new_password,
            password_confirmation=self.password_confirmation,
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name
        )

    def to_user_entity(self) -> UserEntity:
        return UserEntity(
            username=self.username,
            email=self.email,
            password=self.password,
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            password_confirmation=data['password_confirmation'],
            phone_number=data['phone_number'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )


@dataclass
class UserDto:
    id_: int
    username: str
    email: str
    phone_number: str
    first_name: str
    last_name: str

    def to_dict(self) -> dict[str, int | str]:
        return {
            'id': self.id_,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    @classmethod
    def from_user_entity(cls, user_entity: UserEntity) -> Self:
        return cls(
            user_entity.id_,
            user_entity.username,
            user_entity.email,
            user_entity.phone_number,
            user_entity.first_name,
            user_entity.last_name
        )

    def to_client_entity(self) -> ClientEntity:
        return ClientEntity(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone_number=self.phone_number,
            latitude=41.8781,
            longitude=-87.6298,
            user_id=self.id_
        )
