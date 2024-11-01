from src.database import MySQLConnectionManager, with_db_connection
from src.entity import Package, ParcelLocker, Locker, Client
from src.execute_sql_file import SqlFileExecutor
from src.repository import ClientRepository, PackageRepository, LockerRepository, ParcelLockerRepository
import pytest
import os
from datetime import datetime


@pytest.fixture(scope='module')
def connection_manager() -> MySQLConnectionManager:
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '3308'
    os.environ['DB_USER'] = 'user'
    os.environ['DB_PASSWORD'] = 'user1234'
    os.environ['DB_NAME'] = 'db_1'
    os.environ['DB_POOL_SIZE'] = '5'
    return MySQLConnectionManager()


@pytest.fixture(scope='module', autouse=True)
def setup_database_schema(connection_manager) -> None:
    executor = SqlFileExecutor(connection_manager)
    executor.execute_sql_file(os.path.join(os.path.dirname(__file__), '../sql/schema.sql'))


@pytest.fixture
def client_repository(connection_manager) -> ClientRepository:
    return ClientRepository(connection_manager)


@pytest.fixture
def package_repository(connection_manager) -> PackageRepository:
    return PackageRepository(connection_manager)


@pytest.fixture
def locker_repository(connection_manager) -> LockerRepository:
    return LockerRepository(connection_manager)


@pytest.fixture
def parcel_locker_repository(connection_manager) -> ParcelLockerRepository:
    return ParcelLockerRepository(connection_manager)


def test_insert_client(client_repository):
    expected_first_name, expected_last_name = 'Jan', 'Kowalski'
    expected_email, expected_phone = 'jan.kowalski@example.com', '223556789'
    expected_latitude, expected_longitude = 52.2297, 21.0122

    client = Client(
        first_name=expected_first_name,
        last_name=expected_last_name,
        email=expected_email,
        phone_number=expected_phone,
        latitude=expected_latitude,
        longitude=expected_longitude
    )
    client_id = client_repository.insert(client)
    assert client_id is not None

    retrieved_client = client_repository.find_by_id(client_id)
    assert retrieved_client.first_name == expected_first_name
    assert retrieved_client.last_name == expected_last_name
    assert retrieved_client.email == expected_email
    assert retrieved_client.phone_number == expected_phone
    assert retrieved_client.latitude == expected_latitude
    assert retrieved_client.longitude == expected_longitude


def test_insert_parcel_locker(parcel_locker_repository):
    expected_city, expected_postal_code = 'Warsaw', '00-001'
    expected_latitude, expected_longitude = 52.2297, 21.0122
    expected_available_slots = 10

    parcel_locker = ParcelLocker(
        city=expected_city,
        postal_code=expected_postal_code,
        latitude=expected_latitude,
        longitude=expected_longitude,
        available_slots=expected_available_slots
    )
    locker_id = parcel_locker_repository.insert(parcel_locker)
    assert locker_id is not None

    retrieved_locker = parcel_locker_repository.find_by_id(locker_id)
    assert retrieved_locker.city == expected_city
    assert retrieved_locker.postal_code == expected_postal_code
    assert retrieved_locker.latitude == expected_latitude
    assert retrieved_locker.longitude == expected_longitude
    assert retrieved_locker.available_slots == expected_available_slots


def test_insert_package(package_repository):
    expected_sender_id, expected_receiver_id = 1, 2
    expected_parcel_locker_id, expected_locker_id = 1, 1
    expected_status = 'Pending'
    expected_size = 'L'
    expected_created_at = datetime(2024, 11, 1, 14, 24, 20)
    expected_delivered_at = datetime(2024, 12, 1, 14, 24, 20)

    package = Package(
        sender_id=expected_sender_id,
        receiver_id=expected_receiver_id,
        parcel_locker_id=expected_parcel_locker_id,
        locker_id=expected_locker_id,
        status=expected_status,
        size=expected_size,
        delivered_at=expected_delivered_at,
        created_at=expected_created_at,
    )

    package_id = package_repository.insert(package)
    assert package_id is not None

    retrieved_package = package_repository.find_by_id(package_id)

    assert retrieved_package.sender_id == expected_sender_id
    assert retrieved_package.receiver_id == expected_receiver_id
    assert retrieved_package.parcel_locker_id == expected_parcel_locker_id
    assert retrieved_package.locker_id == expected_locker_id
    assert retrieved_package.status == expected_status
    assert retrieved_package.size == expected_size
    assert retrieved_package.delivered_at == expected_delivered_at
    assert retrieved_package.created_at == expected_created_at


def test_insert_locker(locker_repository):
    expected_parcel_locker_id = 1
    expected_package_id = 1
    expected_client_id = 1
    expected_size = 'M'

    locker = Locker(
        parcel_locker_id=expected_parcel_locker_id,
        package_id=expected_package_id,
        client_id=expected_client_id,
        size=expected_size,
    )

    locker_id = locker_repository.insert(locker)
    assert locker_id is not None

    retrieved_locker = locker_repository.find_by_id(locker_id)

    assert retrieved_locker.parcel_locker_id == expected_parcel_locker_id
    assert retrieved_locker.package_id == expected_package_id
    assert retrieved_locker.client_id == expected_client_id
    assert retrieved_locker.size == expected_size



