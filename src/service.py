from src.entity import Package
from src.repository import LockerRepository, ClientRepository, ParcelLockerRepository, PackageRepository
from dataclasses import dataclass
from src.database import with_db_connection, MySQLConnectionManager
import math


@dataclass
class ParcelLockerService:
    def __init__(self, locker_repo: LockerRepository, client_repo: ClientRepository, package_repo: PackageRepository,
                 parcel_locker_repo: ParcelLockerRepository, connection_manager: MySQLConnectionManager):
        self.locker_repo = locker_repo
        self.client_repo = client_repo
        self.package_repo = package_repo
        self.parcel_locker_repo = parcel_locker_repo
        self._connection_manager = connection_manager

    def find_client_location(self, client_id: int) -> tuple[float, float]:
        client = self.client_repo.find_by_id(client_id)
        return client.latitude, client.longitude

    @with_db_connection
    def find_nearest_parcel_lockers(self, client_id: int, max_distance: float) -> list[tuple[int, ...]]:
        client_location = self.client_repo.find_by_id(client_id)
        table_name = self.parcel_locker_repo.table_name()

        sql = (f"WITH DistanceCalc AS ( "
               f"SELECT {table_name}.id_, {table_name}.city, "
               f"(6371.0 * 2 * ASIN(SQRT(POWER(SIN((RADIANS(%s) - RADIANS(latitude)) / 2), 2) + "
               f"COS(RADIANS(%s)) * COS(RADIANS(latitude)) * "
               f"POWER(SIN((RADIANS(%s) - RADIANS(longitude)) / 2), 2)))) AS distance "
               f"FROM {table_name} ) SELECT id_, city, distance FROM DistanceCalc WHERE distance < %s "
               f"ORDER BY distance;")

        self._cursor.execute(sql, (client_location.latitude, client_location.latitude, client_location.longitude,
                                   max_distance))
        result = self._cursor.fetchall()
        return sorted(result, key=lambda x: x[2])


