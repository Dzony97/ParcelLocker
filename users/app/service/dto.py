from dataclasses import dataclass
from app.db.entity import UserEntity
from typing import Self


@dataclass
class RegisterUserDto:
    username: str
    password: str
    confirm_password: str
    email: str
    phone_number: str
    first_name: str
    last_name: str

