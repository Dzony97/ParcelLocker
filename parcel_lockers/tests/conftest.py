import os
import pytest
from dotenv import load_dotenv

load_dotenv('.env.test')
from parcel_lockers.main import create_app
from parcel_lockers.app.src.execute_sql_file import SqlFileExecutor
from parcel_lockers.app.src.database import MySQLConnectionManager, with_db_connection


@pytest.fixture(scope='module')
def connection_manager() -> MySQLConnectionManager:
    """
    Fixture that sets up the MySQL connection manager for testing.

    It loads the necessary environment variables for connecting to the database
    and returns an instance of `MySQLConnectionManager` that manages the
    database connection pool.

    :return: An instance of `MySQLConnectionManager` used for database connections.
    """
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '3308'
    os.environ['DB_USER'] = 'user'
    os.environ['DB_PASSWORD'] = 'user1234'
    os.environ['DB_NAME'] = 'db_1'
    os.environ['DB_POOL_SIZE'] = '5'
    return MySQLConnectionManager()


@pytest.fixture(scope='module', autouse=True)
def setup_database_schema(connection_manager) -> None:
    """
    Fixture to set up the database schema for testing.

    This fixture automatically runs before the tests start. It initializes the
    database schema by executing the SQL file `schema.sql`, which should
    contain the required structure (tables, relations, etc.) for the tests.

    :param connection_manager: The connection manager used to interact with the database.
    """
    executor = SqlFileExecutor(connection_manager)
    executor.execute_sql_file(os.path.join(os.path.dirname(__file__), '../app/sql/schema.sql'))


@pytest.fixture(scope='session')
def app():
    test_app = create_app()
    test_app.config['TESTING'] = True
    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(app):
    return app.test_client()
