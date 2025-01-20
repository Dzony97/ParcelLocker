from app.db.configuration import sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
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
    __tablename__ = 'users'

    id_: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(512), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(55), nullable=False)
    last_name: Mapped[str] = mapped_column(String(55), nullable=False)


class ClientEntity(sa.Model):
    __tablename__ = 'client'

    id_: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(55), nullable=False)
    last_name: Mapped[str] = mapped_column(String(55), nullable=False)
    email: Mapped[str] = mapped_column(String(55), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(sa.ForeignKey('users.phone_number'))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    user: Mapped[UserEntity] = sa.relationship('UserEntity', uselist=False)


class ActivationTokenEntity(sa.Model):
    __tablename__ = 'activation_tokens'

    id_: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[int] = mapped_column(BigInteger)

    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id_'))
    user: Mapped[UserEntity] = sa.relationship('UserEntity', uselist=False)

    def is_active(self) -> bool:
        return self.timestamp > datetime.datetime.now(datetime.UTC).timestamp()

    @staticmethod
    def generate_token(size: int) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join([random.choice(characters) for _ in range(size)])

