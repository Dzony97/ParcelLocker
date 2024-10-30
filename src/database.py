from dotenv import load_dotenv
from mysql.connector import pooling, MySQLConnection
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




