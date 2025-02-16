from parcel_lockers.app.src.service import ParcelLockerService
from parcel_lockers.app.src.repository import LockerRepository, ClientRepository, PackageRepository, ParcelLockerRepository
from parcel_lockers.app.src.database import MySQLConnectionManager

connection_manager = MySQLConnectionManager()
locker_repo = LockerRepository(connection_manager)
client_repo = ClientRepository(connection_manager)
package_repo = PackageRepository(connection_manager)
parcel_locker_repo = ParcelLockerRepository(connection_manager, client_repo)


parcel_locker_service = ParcelLockerService(
    locker_repo=locker_repo,
    client_repo=client_repo,
    package_repo=package_repo,
    parcel_locker_repo=parcel_locker_repo,
    connection_manager=connection_manager
)
