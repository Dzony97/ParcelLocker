from dotenv import load_dotenv
from mysql.connector import pooling, MySQLConnection
from typing import Callable, Any

import os

load_dotenv()


class MySQLConnectionManager:
    """
    Manages a pool of MySQL database connections.

    This class creates a connection pool using environment variables to configure the database connection.
    Connections can be obtained from the pool for use in database operations.
    """

    def __init__(self):
        """
        Initializes the connection pool for MySQL.

        Environment variables used:
        - DB_POOL_SIZE: The size of the connection pool (default: 5).
        - DB_HOST: Hostname of the MySQL server.
        - DB_NAME: Name of the database to connect to.
        - DB_USER: Username for database authentication.
        - DB_PASSWORD: Password for database authentication.
        - DB_PORT: Port for connecting to the database (default: 3307).
        """
        self._pool = pooling.MySQLConnectionPool(
            pool_name='mysql_pool',
            pool_size=int(os.getenv('DB_POOL_SIZE', 5)),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 3307))
        )

    def get_connection(self) -> MySQLConnection:
        """
        Retrieves a connection from the pool.

        :return: A MySQLConnection instance.
        """
        return self._pool.get_connection()


def with_db_connection(func: Callable) -> Callable:
    """
    Decorator to manage database connection and cursor lifecycle.

    This decorator wraps a function, providing it with a database connection and cursor.
    It ensures proper connection management, including committing transactions or rolling back in case of exceptions.

    :param func: The function to wrap, which expects access to `self._conn` and `self._cursor`.
    :return: The wrapped function.
    """
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        """
        Wrapper function that injects a database connection and cursor into the wrapped function.

        :param self: Instance of the class containing the wrapped method.
        :param args: Positional arguments for the wrapped function.
        :param kwargs: Keyword arguments for the wrapped function.
        :return: The result of the wrapped function.
        :raises Exception: Propagates any exceptions after rolling back the transaction.
        """
        with (self._connection_manager.get_connection() as conn,
              conn.cursor() as cursor):
            try:
                self._conn = conn
                self._cursor = cursor
                result = func(self, *args, **kwargs)
                self._conn.commit()
                return result
            except Exception as e:
                if self._conn:
                    self._conn.rollback()
                raise e

    return wrapper

