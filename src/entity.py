from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Self, override


@dataclass
class Entity(ABC):
    id_: int | None = None

    @classmethod
    @abstractmethod
    def from_row(cls, *args) -> Self:
        pass


@dataclass
class Client(Entity):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    @classmethod
    @override
    def from_row(cls, *args) -> Self:
        return cls(
            id_=int(args[0]),
            first_name=args[1],
            last_name=args[2],
            email=args[3],
            phone_number=args[4],
            latitude=float(args[5]),
            longitude=float(args[6])
        )


@dataclass
class ParcelLocker(Entity):
    city: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    available_slots: int | None = None

    @classmethod
    @override
    def from_row(cls, *args) -> Self:
        return cls(
            id_=int(args[0]),
            city=args[1],
            postal_code=args[2],
            latitude=float(args[3]),
            longitude=float(args[4]),
            available_slots=int(args[5])
        )


@dataclass
class Package(Entity):
    sender_id: int | None = None
    receiver_id: int | None = None
    parcel_locker_id: int | None = None
    locker_id: int | None = None
    status: str | None = None
    size: str | None = None
    delivered_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)

    @classmethod
    @override
    def from_row(cls, *args) -> Self:
        return cls(
            id_=int(args[0]),
            sender_id=int(args[1]),
            receiver_id=int(args[2]),
            parcel_locker_id=int(args[3]),
            locker_id=int(args[4]),
            status=args[5],
            size=args[6],
            delivered_at=args[7],
            created_at=args[8]
        )


@dataclass
class Locker(Entity):
    parcel_locker_id: int | None = None
    package_id: int | None = None
    client_id: int | None = None
    size: str | None = None

    @classmethod
    @override
    def from_row(cls, *args) -> Self:
        return cls(
            id_=int(args[0]),
            parcel_locker_id=int(args[1]),
            package_id=int(args[2]),
            client_id=int(args[3]),
            size=args[4]
        )