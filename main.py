from src.database import MySQLConnectionManager
from src.repository import PackageRepository, ClientRepository, LockerRepository, ParcelLockerRepository
from src.service import ParcelLockerService
from src.entity import Size


def main() -> None:
    my_sql_connection_manager = MySQLConnectionManager()
    locker_repository = LockerRepository(my_sql_connection_manager)
    package_repository = PackageRepository(my_sql_connection_manager)
    client_repository = ClientRepository(my_sql_connection_manager)
    parcel_locker_repository = ParcelLockerRepository(my_sql_connection_manager)
    parcel_locker_service = ParcelLockerService(locker_repository, client_repository,
                                                package_repository, parcel_locker_repository, my_sql_connection_manager)
    print(parcel_locker_service.find_nearest_parcel_lockers(1, 600))
    print(parcel_locker_service.send_package(1, 3, 9600, Size.S.value))


if __name__ == '__main__':
    main()
