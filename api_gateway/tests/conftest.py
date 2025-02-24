import pytest
from main import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "JWT_SECRET": "test_secret",
        "JWT_ISSUER": "test_issuer",
        "JWT_AUTHTYPE": "HS256",
        "JWT_ACCESS_MAX_AGE": 5,
        "JWT_REFRESH_MAX_AGE": 5,
        "JWT_PREFIX": "Bearer"
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()