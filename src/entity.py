from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Self, override
from enum import Enum


@dataclass
class Entity(ABC):
    """
    Abstract base class for all entities in the system.

    Provides a common structure for entities, including an optional ID field and
    an abstract method for creating instances from database rows.
    """
    id_: int | None = None

    @classmethod
    @abstractmethod
    def from_row(cls, *args) -> Self:
        """
        Abstract method to construct an entity instance from a database row.

        :param args: The row data from the database.
        :return: An instance of the entity.
        """
        pass


@dataclass
class Client(Entity):
    """
    Represents a client in the system.

    Stores client information including name, contact details, and geographical location.
    """
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    @classmethod
    @override
    def from_row(cls, *args) -> Self:
        """
        Creates a Client instance from a database row.

        :param args: The row data from the database.
        :return: A Client instance.
        """
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
    """
    Represents a parcel locker in the system.

    Stores information about the location of the parcel locker.
    """
    city: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    @classmethod
    @override
    def from_row(cls, *args) -> Self:
        """
        Creates a ParcelLocker instance from a database row.

        :param args: The row data from the database.
        :return: A ParcelLocker instance.
        """
        return cls(
            id_=int(args[0]),
            city=args[1],
            postal_code=args[2],
            latitude=float(args[3]),
            longitude=float(args[4])
        )


@dataclass
class Package(Entity):
    """
    Represents a package in the system.

    Stores information about the package sender, receiver, locker, status, size, and timestamps.
    """
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
        """
        Creates a Package instance from a database row.

        :param args: The row data from the database.
        :return: A Package instance.
        """
        print(f"Row data received in from_row: {args}")
        return cls(
            id_=int(args[0]),
            sender_id=int(args[1]),
            receiver_id=int(args[2]),
            parcel_locker_id=int(args[3]),
            locker_id=int(args[4]) if args[4] is not None else None,
            status=args[8],
            size=args[5],
            delivered_at=args[7],
            created_at=args[6]
        )


@dataclass
class Locker(Entity):
    """
    Represents a locker in a parcel locker system.

    Stores information about the locker, including its associated parcel locker, package, size, and status.
    """
    parcel_locker_id: int | None = None
    package_id: int | None = None
    client_id: int | None = None
    size: str | None = None
    status: str | None = None

    @classmethod
    @override
    def from_row(cls, *args) -> Self:
        """
        Creates a Locker instance from a database row.

        :param args: The row data from the database.
        :return: A Locker instance.
        """
        return cls(
            id_=int(args[0]),
            parcel_locker_id=int(args[1]),
            package_id=int(args[2]) if args[2] is not None else None,
            client_id=int(args[3]) if args[3] is not None else None,
            size=args[4],
            status=args[5]
        )


class Size(Enum):
    """
    Enum representing the sizes of lockers available in the parcel locker system.
    """
    S = 'S'
    M = 'M'
    L = 'L'

