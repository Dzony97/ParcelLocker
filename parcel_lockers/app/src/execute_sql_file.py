from mysql.connector import Error
from parcel_lockers.app.src.database import MySQLConnectionManager, with_db_connection


class SqlFileExecutor:
    """
    A utility class for executing SQL commands from a file.

    This class provides functionality to read and execute SQL commands from a file,
    leveraging a database connection managed by `MySQLConnectionManager`.
    """

    def __init__(self, connection_manager: MySQLConnectionManager):
        """
        Initializes the SqlFileExecutor with a connection manager.

        :param connection_manager: An instance of `MySQLConnectionManager` for managing database connections.
        """
        self._connection_manager = connection_manager

    @with_db_connection
    def execute_sql_file(self, sql_file: str):
        """
        Executes all SQL commands in the specified file.

        The method reads the file, splits its contents into individual SQL commands,
        and executes them sequentially using the database connection.

        :param sql_file: Path to the SQL file containing commands to execute.
        :raises Error: If an error occurs during the execution of SQL commands.
        """
        with open(sql_file, 'r') as sql_file:
            sql_command = sql_file.read()

        try:
            for command in sql_command.split(';'):
                command = command.strip()
                if command:
                    self._cursor.execute(command)
        except Error as e:
            raise e
