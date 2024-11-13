import pytest
from src.service import ParcelLockerService
from src.repository import LockerRepository, ClientRepository, PackageRepository, ParcelLockerRepository
from src.entity import Size

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
    excepted_location = parcel_locker_service.find_client_location(5)
    assert excepted_location == (52.2297, 21.0122)


def test_has_available_slots(parcel_locker_service):
    excepted_result = parcel_locker_service.has_available_slots(Size.S.value, 1)
    assert excepted_result == [1, 2]


def test_find_nearest_parcel_lockers(parcel_locker_service):
    excepted_result = parcel_locker_service.find_nearest_parcel_lockers(1, 10)
    assert excepted_result == [(1, 'San Francisco', 0.035427176436514)]


def

