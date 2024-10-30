from src.entity import Entity, Client, Locker, ParcelLocker, Package
from src.database import with_db_connection, MySQLConnectionManager
from typing import Type

import inflection


class CrudRepository[T: Entity]:
    def __init__(self, connection_manager: MySQLConnectionManager, entity_type: Type[T]):
        self._connection_manager = connection_manager
        self._entity_type = entity_type


    def _table_name(self) -> str:
        return inflection.underscore(self._entity_type.__name__)

    def _column_names_for_insert(self) -> str:
        return ', '.join([field for field in self._entity_type.__annotations__.keys()])

    def _column_values_for_insert(self, item: T) -> str:
        fields = [field for field in self._entity_type.__annotations__.keys()]
        values = [
            str(getattr(item, field)) if isinstance(getattr(item, field), (int, float))
            else f"'{getattr(item, field)}'"
            for field in fields
        ]
        return ', '.join(values)

    def _column_names_and_values_for_update(self, item: T) -> str:
        return ', '.join([
            f"{field} = {str(getattr(item, field)) if isinstance(getattr(item, field), (int, float))
            else f"'{getattr(item, field)}'"}"
            for field in self._entity_type.__annotations__.keys()
            if field != 'id_'
        ])