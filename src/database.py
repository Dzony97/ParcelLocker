from dotenv import load_dotenv
from mysql.connector import pooling, MySQLConnection
from typing import Callable, Any
import os

load_dotenv()


class MySQLConnectionManager:
    def __init__(self):
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
        return self._pool.get_connection()


def with_db_connection(func: Callable) -> Callable:
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
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
