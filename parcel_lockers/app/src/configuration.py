from app.src.database import MySQLConnectionManager
from app.src.repository import (
    LockerRepository,
    ClientRepository,
    PackageRepository,
    ParcelLockerRepository,
)
from app.src.service import ParcelLockerService


def create_parcel_locker_service() -> ParcelLockerService:
    """
    Creates and returns an instance of ParcelLockerService with initialized repositories.

    :return: An instance of ParcelLockerService.
    """
    connection_manager = MySQLConnectionManager()
    locker_repo = LockerRepository(connection_manager)
    client_repo = ClientRepository(connection_manager)
    package_repo = PackageRepository(connection_manager)
    parcel_locker_repo = ParcelLockerRepository(connection_manager, client_repo)

    return ParcelLockerService(
        locker_repo=locker_repo,
        client_repo=client_repo,
        package_repo=package_repo,
        parcel_locker_repo=parcel_locker_repo,
        connection_manager=connection_manager
    )
