from app.db.configuration import sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from werkzeug.security import check_password_hash
from sqlalchemy import (
    String,
    Boolean,
    Integer,
    Float,
    DateTime,
    BigInteger
)
import datetime
import logging
import random
import string

logging.basicConfig(level=logging.INFO)

class UserEntity(sa.Model):
    """
    Represents a user entity in the database.

    Attributes:
        id_ (int): Primary key, auto-incremented unique identifier for the user.
        username (str): Unique username of the user.
        password (str): Hashed password of the user.
        email (str): Unique email address of the user.
        phone_number (str): Unique phone number associated with the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        role (str): Role of the user (e.g., admin, client).
        is_active (bool): Indicates whether the user account is active.
    """

    __tablename__ = 'users'

    id_: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(512), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(55), nullable=False)
    last_name: Mapped[str] = mapped_column(String(55), nullable=False)
    role: Mapped[str] = mapped_column(String(10))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self) -> str:
        """
        Returns a string representation of the UserEntity instance.
        """
        return f'USER ENTITY: {self.id_}, {self.username}'

    def __repr__(self):
        """
        Returns a formal string representation of the UserEntity instance.
        """
        return str(self)

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the stored hashed password.

        Args:
            password (str): The plain text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)


class ClientEntity(sa.Model):
    """
    Represents a client entity in the database.

    Attributes:
        id_ (int): Primary key, auto-incremented unique identifier for the client.
        first_name (str): First name of the client.
        last_name (str): Last name of the client.
        email (str): Unique email of the client.
        phone_number (str): Phone number associated with the client (linked to users).
        latitude (float): Latitude of the client's location (optional).
        longitude (float): Longitude of the client's location (optional).
    """

    __tablename__ = 'client'

    id_: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(55), nullable=False)
    last_name: Mapped[str] = mapped_column(String(55), nullable=False)
    email: Mapped[str] = mapped_column(String(55), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(sa.ForeignKey('users.phone_number'))
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    user: Mapped[UserEntity] = sa.relationship('UserEntity', uselist=False)

    def __str__(self) -> str:
        """
        Returns a string representation of the ClientEntity instance.
        """
        return f'CLIENT ENTITY: {self.id_}, {self.first_name} {self.last_name}'

    def __repr__(self):
        """
        Returns a formal string representation of the ClientEntity instance.
        """
        return str(self)


class ActivationTokenEntity(sa.Model):
    """
    Represents an activation token entity in the database.

    Activation tokens are used to verify user accounts.

    Attributes:
        id_ (int): Primary key of the activation token.
        token (str): The activation token string.
        timestamp (int): Timestamp (Unix time) indicating the token's expiration.
        user_id (int): Foreign key linking the token to a specific user.
        user (UserEntity): Relationship linking the token to the UserEntity.
    """

    __tablename__ = 'activation_tokens'

    id_: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[int] = mapped_column(BigInteger)

    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id_'))
    user: Mapped[UserEntity] = sa.relationship('UserEntity', uselist=False)

    def is_active(self) -> bool:
        """
        Checks if the activation token is still active.

        Returns:
            bool: True if the token has not expired, False otherwise.
        """
        return self.timestamp > datetime.datetime.now(datetime.UTC).timestamp()

    @staticmethod
    def generate_token(size: int) -> str:
        """
        Generates a random activation token of the specified length.

        Args:
            size (int): The length of the token.

        Returns:
            str: A randomly generated token containing letters and digits.
        """
        characters = string.ascii_letters + string.digits
        return ''.join([random.choice(characters) for _ in range(size)])
