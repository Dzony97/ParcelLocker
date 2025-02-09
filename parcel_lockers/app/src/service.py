from app.src.repository import LockerRepository, ClientRepository, ParcelLockerRepository, PackageRepository
from app.src.database import MySQLConnectionManager
from app.src.entity import Package, ParcelLocker, Locker
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ParcelLockerService:
    """
    Service class for managing parcel locker operations.

    This class provides functionality for finding client locations, checking locker availability,
    sending and receiving packages, and finding nearest parcel lockers.
    """

    def __init__(self, locker_repo: LockerRepository, client_repo: ClientRepository, package_repo: PackageRepository,
                 parcel_locker_repo: ParcelLockerRepository, connection_manager: MySQLConnectionManager):
        """
        Initializes the ParcelLockerService with repository and connection manager dependencies.

        :param locker_repo: Repository for managing lockers.
        :param client_repo: Repository for managing client data.
        :param package_repo: Repository for managing packages.
        :param parcel_locker_repo: Repository for managing parcel lockers.
        :param connection_manager: Database connection manager.
        """
        self.locker_repo = locker_repo
        self.client_repo = client_repo
        self.package_repo = package_repo
        self.parcel_locker_repo = parcel_locker_repo
        self._connection_manager = connection_manager

    def find_client_location(self, client_id: int) -> tuple[float, float]:
        """
        Finds the geographical location of a client by ID.

        :param client_id: The ID of the client.
        :return: A tuple containing the latitude and longitude of the client.
        """
        client = self.client_repo.find_by_id(client_id)
        return client.latitude, client.longitude

    def send_package(self, client_id: int, receiver_id: int, max_distance: float, size: Enum) -> Package:
        """
        Sends a package to the nearest parcel locker with available slots.

        :param client_id: The ID of the sender.
        :param receiver_id: The ID of the receiver.
        :param max_distance: The maximum distance to search for parcel lockers.
        :param size: Size of the package.
        :return: The created Package instance.
        :raises ValueError: If no parcel lockers or available slots are found.
        """
        parcel_lockers = self.parcel_locker_repo.find_nearest_parcel_lockers(client_id, max_distance)
        if not parcel_lockers:
            raise ValueError("No parcel lockers found")

        for parcel_locker in parcel_lockers:
            available_slots = self.locker_repo.has_available_slots(size, parcel_locker[0])
            if available_slots:
                package = Package(
                    sender_id=client_id,
                    receiver_id=receiver_id,
                    parcel_locker_id=parcel_locker[0],
                    locker_id=available_slots[0],
                    status="In locker",
                    size=str(size),
                    created_at=datetime.now()
                )
                package = self.package_repo.insert(package)
                locker_to_use = self.locker_repo.find_by_id(available_slots[0])
                locker_to_use.status, locker_to_use.package_id, locker_to_use.client_id \
                    = "Occupied", package, receiver_id
                self.locker_repo.update(locker_to_use.id_, locker_to_use)
                return package
        raise ValueError("No available slots found")

    def receive_package(self, package_id: int) -> None:
        """
        Marks a package as received and updates the locker status to available.

        :param package_id: The ID of the package to receive.
        :raises ValueError: If the package or its associated locker is not found.
        """
        package = self.package_repo.find_by_id(package_id)
        locker_to_use = self.locker_repo.find_by_id(package.locker_id)

        if not package:
            raise ValueError("No package found")
        if not locker_to_use:
            raise ValueError("No locker_to_use found")

        package.status = "Received"
        package.delivered_at = datetime.now()
        self.package_repo.update(package_id, package)

        locker_to_use.status = "Available"
        locker_to_use.package_id = None
        locker_to_use.client_id = None
        self.locker_repo.update(locker_to_use.id_, locker_to_use)

    def add_parcel_locker(self, city: str, postal_code: str, latitude: float, longitude: float) -> int:
        """
        Creates a new ParcelLocker object and inserts it into the database.

        :param city: The name of the city where the parcel locker is located
        :param postal_code: The postal code of the parcel locker
        :param latitude: The latitude coordinate
        :param longitude: The longitude coordinate
        :return: The ID of the newly added record in the database
        """
        parcel_locker = ParcelLocker(
            city=city,
            postal_code=postal_code,
            latitude=latitude,
            longitude=longitude
        )

        new_parcel_locker = self.parcel_locker_repo.insert(parcel_locker)
        return new_parcel_locker

    def add_locker(self, parcel_locker_id: int, package_id: int | None, client_id: int | None, size: str,
                   status: str) -> Locker:
        """
        Creates a new Locker object and inserts it into the database.

        :param parcel_locker_id: The ID of the parcel locker this locker belongs to.
        :param package_id: The ID of the package inside this locker (optional).
        :param client_id: The ID of the client (optional).
        :param size: The size of the locker (e.g., S, M, L).
        :param status: The status of the locker (e.g., 'EMPTY', 'OCCUPIED').
        :return: The ID of the newly added record in the database.
        """
        locker = Locker(
            parcel_locker_id=parcel_locker_id,
            package_id=package_id,
            client_id=client_id,
            size=size,
            status=status
        )

        new_locker = self.locker_repo.insert(locker)
        return new_locker
