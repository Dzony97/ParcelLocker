from src.execute_sql_file import SqlFileExecutor
from src.database import MySQLConnectionManager, with_db_connection
import os
import pytest


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