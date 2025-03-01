from dataclasses import dataclass
from app.db.entity import UserEntity, ClientEntity
from typing import Self


@dataclass
class RegisterUserDto:
    """
    Data Transfer Object (DTO) for registering a new user.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        password_confirmation (str): The confirmation of the password.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        role (str): The role of the user (e.g., 'admin', 'client').
    """

    username: str
    password: str
    password_confirmation: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
    role: str

    def check_passwords(self) -> bool:
        """
        Checks if the password and password confirmation match.

        Returns:
            bool: True if passwords match, False otherwise.
        """
        return self.password == self.password_confirmation

    def with_password(self, new_password: str) -> Self:
        """
        Creates a new instance of the RegisterUserDto with a different password.

        Args:
            new_password (str): The new password.

        Returns:
            RegisterUserDto: A new instance with the updated password.
        """
        return RegisterUserDto(
            username=self.username,
            email=self.email,
            password=new_password,
            password_confirmation=self.password_confirmation,
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role
        )

    def to_user_entity(self) -> UserEntity:
        """
        Converts the RegisterUserDto to a UserEntity.

        Returns:
            UserEntity: The corresponding UserEntity.
        """
        return UserEntity(
            username=self.username,
            email=self.email,
            password=self.password,
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        """
        Creates an instance of RegisterUserDto from a dictionary.

        Args:
            data (dict[str, str]): A dictionary containing user registration data.

        Returns:
            RegisterUserDto: A new instance populated from the provided dictionary.
        """
        return cls(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            password_confirmation=data['password_confirmation'],
            phone_number=data['phone_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role']
        )


@dataclass
class UserDto:
    """
    Data Transfer Object (DTO) for a user entity.

    Attributes:
        id_ (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        role (str): The role of the user (e.g., 'admin', 'client').
    """

    id_: int
    username: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
    role: str

    def to_dict(self) -> dict[str, int | str]:
        """
        Converts the UserDto to a dictionary.

        Returns:
            dict[str, int | str]: A dictionary representation of the UserDto.
        """
        return {
            'id': self.id_,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role
        }

    @classmethod
    def from_user_entity(cls, user_entity: UserEntity) -> Self:
        """
        Creates a UserDto instance from a UserEntity.

        Args:
            user_entity (UserEntity): The UserEntity to convert.

        Returns:
            UserDto: The corresponding UserDto instance.
        """
        return cls(
            user_entity.id_,
            user_entity.username,
            user_entity.email,
            user_entity.phone_number,
            user_entity.first_name,
            user_entity.last_name,
            user_entity.role
        )

    @classmethod
    def to_client_entity(cls, user_entity: UserEntity) -> ClientEntity:
        """
        Converts a UserEntity to a ClientEntity.

        Args:
            user_entity (UserEntity): The UserEntity to convert.

        Returns:
            ClientEntity: The corresponding ClientEntity.
        """
        return ClientEntity(
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            email=user_entity.email,
            phone_number=user_entity.phone_number,
            latitude=None,
            longitude=None
        )
