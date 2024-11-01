from src.database import MySQLConnectionManager
from src.repository import PackageRepository, ClientRepository, LockerRepository, ParcelLockerRepository


def main() -> None:
    my_sql_connection_manager = MySQLConnectionManager()
    locker_repository = LockerRepository(my_sql_connection_manager)
    package_repository = PackageRepository(my_sql_connection_manager)
    client_repository = ClientRepository(my_sql_connection_manager)
    parcel_locker_repository = ParcelLockerRepository(my_sql_connection_manager)


if __name__ == '__main__':
    main()
