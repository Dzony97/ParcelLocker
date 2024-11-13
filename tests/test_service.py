import pytest
from src.service import ParcelLockerService
from src.repository import LockerRepository, ClientRepository, PackageRepository, ParcelLockerRepository
from src.database import MySQLConnectionManager


@pytest.fixture
def parcel_locker_service(connection_manager) -> ParcelLockerService:
    locker_repo = LockerRepository(connection_manager)
    client_repo = ClientRepository(connection_manager)
    package_repo = PackageRepository(connection_manager)
    parcel_locker_repo = ParcelLockerRepository(connection_manager)

    return ParcelLockerService(
        locker_repo=locker_repo,
        client_repo=client_repo,
        package_repo=package_repo,
        parcel_locker_repo=parcel_locker_repo,
        connection_manager=connection_manager
    )


def test_find_client_location(parcel_locker_service):
    client_location = parcel_locker_service.find_client_location(5)
    assert client_location == (52.2297, 21.0122)



