import pytest
from app.src.service import ParcelLockerService
from app.src.repository import LockerRepository, ClientRepository, PackageRepository, ParcelLockerRepository
from app.src.entity import Size
from datetime import datetime


@pytest.fixture
def parcel_locker_service(connection_manager) -> ParcelLockerService:
    """
    Fixture to create and provide a `ParcelLockerService` instance for tests.

    :param connection_manager: The connection manager used to interact with the database.
    :return: A `ParcelLockerService` instance for performing business logic related to parcel lockers.
    """
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


def test_find_client_location(parcel_locker_service):
    """
    Test to verify that the `find_client_location` method returns the correct coordinates of a client.

    :param parcel_locker_service: The service that manages the business logic related to parcel lockers.
    """
    expected_location = parcel_locker_service.find_client_location(1)
    assert expected_location == (52.2297, 21.0122)


def test_send_package(parcel_locker_service):
    """
    Test to verify that the `send_package` method correctly processes the sending of a package.

    :param parcel_locker_service: The service that manages the business logic related to parcel lockers.
    """
    expected_result = parcel_locker_service.send_package(1, 1, 1000000, Size.S.value)
    assert expected_result == 3


def test_no_parcel_locker_found(parcel_locker_service):
    """
    Test to verify that the `send_package` method raises an exception when no parcel lockers are found.

    :param parcel_locker_service: The service that manages the business logic related to parcel lockers.
    """
    with pytest.raises(ValueError, match="No parcel lockers found"):
        parcel_locker_service.send_package(1, 1, 10, Size.S.value)


def test_receive_package(parcel_locker_service):
    """
    Test to verify that the `receive_package` method correctly updates
    the package status and locker availability, including a time
    tolerance check for the delivered_at field.
    """

    parcel_locker_service.receive_package(2)

    package = parcel_locker_service.package_repo.find_by_id(2)
    locker = parcel_locker_service.locker_repo.find_by_id(package.locker_id)

    now = datetime.now()
    time_diff = abs((package.delivered_at - now).total_seconds())
    assert time_diff < 5

    assert package.status == "Received"
    assert locker.status == "Available"







