import pytest
from src.service import ParcelLockerService
from src.repository import LockerRepository, ClientRepository, PackageRepository, ParcelLockerRepository
from src.entity import Size
from src.entity import Package
from datetime import datetime


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
    excepted_location = parcel_locker_service.find_client_location(1)
    assert excepted_location == (52.2297, 21.0122)


def test_has_available_slots(parcel_locker_service):
    excepted_result = parcel_locker_service.has_available_slots(Size.S.value, 1)
    assert excepted_result == [1]


def test_find_nearest_parcel_lockers(parcel_locker_service):
    excepted_result = parcel_locker_service.find_nearest_parcel_lockers(1, 1000000)
    assert excepted_result == [(1, 'San Francisco', 9398.916624268912)]


def test_send_package(parcel_locker_service):
    excepted_result = parcel_locker_service.send_package(1, 1, 1000000, Size.S.value)
    assert excepted_result == 2


def test_no_parcel_locker_found(parcel_locker_service):
    with pytest.raises(ValueError, match="No parcel lockers found"):
        parcel_locker_service.send_package(1, 1, 10, Size.S.value)


def test_no_available_slots(parcel_locker_service):
    with pytest.raises(ValueError, match="No available slots found"):
        parcel_locker_service.send_package(1, 1, 1000000, Size.S.value)


def test_receive_package(parcel_locker_service):
    parcel_locker_service.receive_package(2)
    package = parcel_locker_service.package_repo.find_by_id(2)
    locker = parcel_locker_service.locker_repo.find_by_id(package.locker_id)
    assert package.status == "Received"
    assert package.delivered_at.replace(microsecond=0) == datetime.now().replace(microsecond=0)
    assert locker.status == "Available"




