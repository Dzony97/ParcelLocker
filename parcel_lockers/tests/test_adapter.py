import pytest
from dotenv import load_dotenv
from parcel_lockers.app.src.configuration import create_parcel_locker_service

load_dotenv('.env.test')
import os

from parcel_lockers.main import create_app


@pytest.fixture
def app():

    test_app = create_app()
    test_app.config['TESTING'] = True
    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_app_creation(app):
    assert app is not None


def test_create_parcel_locker_service():
    service = create_parcel_locker_service()
    assert service is not None

    assert service._connection_manager is not None
    assert service.client_repo is not None
    assert service.package_repo is not None



