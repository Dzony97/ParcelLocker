from src.entity import ParcelLocker
from src.repository import LockerRepository, ClientRepository, ParcelLockerRepository, PackageRepository
from geopy.distance import geodesic
from typing import Callable
from dataclasses import dataclass


@dataclass
class ParcelLockerService:
    def __init__(self, locker_repo: LockerRepository, client_repo: ClientRepository, package_repo: PackageRepository,
                 parcel_locker_repository: ParcelLockerRepository):
        self.locker_repo = locker_repo
        self.client_repo = client_repo
        self.package_repo = package_repo
        self.parcel_locker_repository = parcel_locker_repository

    def find_client_location(self, client_id: int) -> tuple[float, float]:
        client = self.client_repo.find_by_id(client_id)
        return client.latitude, client.longitude

    def find_nearest_parcel_lockers(self, client_id, max_distance: float) -> list[dict[str, float]]:
        parcel_lockers = self.parcel_locker_repository.find_all()
        nearest_parcel_lockers = []
        client_location = self.find_client_location(client_id)

        for parcel_locker in parcel_lockers:
            parcel_locker_location = parcel_locker.latitude, parcel_locker.longitude
            distance = geodesic(client_location, parcel_locker_location).kilometers
            if distance < max_distance:
                nearest_parcel_lockers.append({
                    "parcel_locker_id": parcel_locker.id_,
                    "distance_km": distance
                })

        return sorted(nearest_parcel_lockers, key=lambda x: x["distance_km"])




