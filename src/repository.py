from src.entity import Entity, Client, Locker, ParcelLocker, Package
from src.database import with_db_connection, MySQLConnectionManager
from typing import Type
import inflection


class CrudRepository[T: Entity]:
    """
    A generic repository class for performing CRUD operations on entities.

    This class provides methods to interact with a MySQL database for the
    basic Create, Read, Update, and Delete operations on a given entity type.
    """
    def __init__(self, connection_manager: MySQLConnectionManager, entity_type: Type[T]):
        """
        Initializes the repository with a database connection manager and an entity type.

        :param connection_manager: An instance of `MySQLConnectionManager` for managing database connections.
        :param entity_type: The type of the entity the repository will manage (e.g., Client, Package, etc.).
        """
        self._connection_manager = connection_manager
        self._entity_type = entity_type

    @with_db_connection
    def find_all(self) -> list[T]:
        """
        Retrieves all records from the database for the entity type.

        :return: A list of entity instances populated with data from the database.
        """
        sql = f"SELECT * FROM {self.table_name()}"
        self._cursor.execute(sql)
        return [self._entity_type.from_row(*row) for row in self._cursor.fetchall()]

    @with_db_connection
    def find_by_id(self, item_id: int) -> T:
        """
        Retrieves a single entity by its ID from the database.

        :param item_id: The ID of the entity to retrieve.
        :return: An entity instance or `None` if not found.
        """
        sql = f"SELECT * FROM {self.table_name()} where id_ = {item_id}"
        self._cursor.execute(sql)
        item = self._cursor.fetchone()
        return self._entity_type.from_row(*item) if item else None

    @with_db_connection
    def insert(self, item: T) -> int:
        """
        Inserts a new entity into the database.

        :param item: The entity to insert.
        :return: The ID of the newly inserted entity.
        """
        sql = (f'insert into {self.table_name()} '
               f'({self._column_names_for_insert()}) '
               f'values ({self._column_values_for_insert(item)})')
        self._cursor.execute(sql)
        return self._cursor.lastrowid

    @with_db_connection
    def insert_many(self, items: list[T]) -> None:
        """
        Inserts multiple entities into the database in a single operation.

        :param items: A list of entities to insert.
        """
        if not items:
            return

        sql = (f'insert into {self.table_name()} ({self._column_names_for_insert()}) '
               f'values {", ".join(self._values_for_insert_many(items))}')
        self._cursor.execute(sql)

    @with_db_connection
    def update(self, item_id: int, item: T) -> None:
        """
        Updates an existing entity in the database.

        :param item_id: The ID of the entity to update.
        :param item: The updated entity data.
        """
        sql = f'update {self.table_name()} set {self._column_names_and_values_for_update(item)} where id_ = {item_id}'
        self._cursor.execute(sql)

    @with_db_connection
    def delete(self, item_id: int) -> int:
        """
        Deletes an entity from the database by its ID.

        :param item_id: The ID of the entity to delete.
        :return: The ID of the deleted entity.
        """
        sql = f'delete from {self.table_name()} where id_ = {item_id}'
        self._cursor.execute(sql)
        return item_id

    def table_name(self) -> str:
        """
        Converts the entity type name to a table name using snake_case.

        :return: The name of the table corresponding to the entity type.
        """
        return inflection.underscore(self._entity_type.__name__)

    def _column_names_for_insert(self) -> str:
        """
        Retrieves the column names for an insert statement, excluding the ID field.

        :return: A comma-separated string of column names.
        """
        return ', '.join([field for field in self._entity_type.__annotations__.keys() if field != '_id'])

    def _column_values_for_insert(self, item: T) -> str:
        """
        Prepares the values for an insert statement, converting each field to a string.

        :param item: The entity instance to insert.
        :return: A comma-separated string of values to insert.
        """
        fields = [field for field in self._entity_type.__annotations__.keys() if field != '_id']
        values = [
            "NULL" if getattr(item, field) is None else
            str(getattr(item, field)) if isinstance(getattr(item, field), (int, float))
            else f"'{getattr(item, field)}'"
            for field in fields
        ]
        return ', '.join(values)

    def _column_names_and_values_for_update(self, item: T) -> str:
        """
        Prepares the column names and values for an update statement.

        :param item: The entity instance to update.
        :return: A comma-separated string of column-value assignments for the update.
        """
        return ', '.join([
            f"{field} = {('NULL' if getattr(item, field) is None else str(getattr(item, field)) if isinstance(getattr(item, field), (int, float))
            else f"'{getattr(item, field)}'")}"
            for field in self._entity_type.__annotations__.keys()
            if field != 'id_'
        ])

    def _values_for_insert_many(self, items: list[T]) -> list[str]:
        """
        Prepares the values for inserting multiple entities in a single operation.

        :param items: A list of entity instances to insert.
        :return: A list of string values for each entity to be inserted.
        """
        return [f"({self._column_values_for_insert(item)})" for item in items]


class ClientRepository(CrudRepository[Client]):
    """
    Repository class for performing CRUD operations on `Client` entities.
    """
    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, Client)


class PackageRepository(CrudRepository[Package]):
    """
    Repository class for performing CRUD operations on `Package` entities.
    """
    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, Package)


class ParcelLockerRepository(CrudRepository[ParcelLocker]):
    """
    Repository class for performing CRUD operations on `ParcelLocker` entities.
    """
    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, ParcelLocker)


class LockerRepository(CrudRepository[Locker]):
    """
    Repository class for performing CRUD operations on `Locker` entities.
    """
    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, Locker)

