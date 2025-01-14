from users.app.db.configuration import sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy import (
    String,
    Numeric,
    Boolean,
    Integer,
    Float,
    BigInteger,
    ForeignKey,
)
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import logging
logging.basicConfig(level=logging.INFO)


class UserEntity(sa.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(512), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(55), nullable=False)
    last_name: Mapped[str] = mapped_column(String(55), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    client: Mapped['Client'] = sa.relationship('Client', uselist=False)


class Client(sa.Model):
    __tablename__ = 'client'

    id_: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(55), nullable=False)
    last_name: Mapped[str] = mapped_column(String(55), nullable=False)
    email: Mapped[str] = mapped_column(String(55), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    user: Mapped['UserEntity'] = sa.relationship('UserEntity')
