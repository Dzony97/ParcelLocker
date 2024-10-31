from src.database import MySQLConnectionManager, with_db_connection
from src.entity import Package, ParcelLocker, Locker, Client
from src.execute_sql_file import SqlFileExecutor
from src.repository import ClientRepository, PackageRepository, LockerRepository, ParcelLockerRepository
import pytest
import os


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
def driver_repository(connection_manager) -> ClientRepository:
    return ClientRepository(connection_manager)


@pytest.fixture
def offense_repository(connection_manager) -> PackageRepository:
    return PackageRepository(connection_manager)


@pytest.fixture
def violation_repository(connection_manager) -> LockerRepository:
    return LockerRepository(connection_manager)


@pytest.fixture
def speed_camera_repository(connection_manager) -> ParcelLockerRepository:
    return ParcelLockerRepository(connection_manager)