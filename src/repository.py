from src.entity import Entity, Client, Locker, ParcelLocker, Package
from src.database import with_db_connection, MySQLConnectionManager
from typing import Type


class CrudRepository[T: Entity]:
    def __init__(self, connection_manager: MySQLConnectionManager, entity_type: Type[T]):
        self._connection_manager = connection_manager
        self._entity_type = entity_type


