import os
import pytest
from dotenv import load_dotenv

load_dotenv('.env.test')
from main import create_app
from app.src.execute_sql_file import SqlFileExecutor
from app.src.database import MySQLConnectionManager, with_db_connection


@pytest.fixture(scope='module')
def connection_manager() -> MySQLConnectionManager:
    """
    Provides a MySQL connection manager for testing.

    This fixture initializes the database connection manager using test-specific
    environment variables to ensure isolation from the production database.

    :return: A `MySQLConnectionManager` instance for database connections.
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
    Sets up the test database schema.

    This fixture executes the `schema.sql` file to initialize the required database
    structure before the tests run.

    :param connection_manager: The database connection manager used to execute the schema setup.
    """
    executor = SqlFileExecutor(connection_manager)
    executor.execute_sql_file(os.path.join(os.path.dirname(__file__), '../app/sql/schema.sql'))


@pytest.fixture(scope='session')
def app():
    """
    Creates and configures the Flask application for testing.

    The application is set to testing mode to enable easier assertions and debugging.

    :return: A Flask application instance.
    """
    test_app = create_app()
    test_app.config['TESTING'] = True
    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(app):
    """
    Provides a test client for the Flask application.

    The test client allows simulating HTTP requests without running a real server.

    :param app: The Flask application instance.
    :return: A Flask test client instance.
    """
    return app.test_client()
