from mysql.connector import Error
from src.database import MySQLConnectionManager, with_db_connection


class SqlFileExecutor:
    def __init__(self, connection_manager: MySQLConnectionManager):
        self._connection_manager = connection_manager

    @with_db_connection
    def execute_sql_file(self, sql_file: str):
        with open (sql_file, 'r') as sql_file:
            sql_command = sql_file.read()

        try:
            for command in sql_command.split(';'):
                command = command.strip()
                if command:
                    self._cursor.execute(command)
        except Error as e:
            raise e