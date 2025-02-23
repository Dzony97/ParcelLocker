import pytest
from app.src.configuration import create_parcel_locker_service


def test_create_parcel_locker_service():
    service = create_parcel_locker_service()
    assert service is not None

    assert service._connection_manager is not None
    assert service.client_repo is not None
    assert service.package_repo is not None



